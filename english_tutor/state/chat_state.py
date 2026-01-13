from datetime import datetime
import reflex as rx

from sqlmodel import select
from ..agents.orchestrator import Orchestrator
from ..models.evaluation import Message
from ..models.user import Session, User
from ..models.content import Curriculum


class ChatState(rx.State):
    """The state for the chat interface."""

    messages: list[dict[str, str]] = []
    input_text: str = ""
    is_recording: bool = False
    is_processing: bool = False

    def set_input_text(self, text: str):
        self.input_text = text

    async def handle_key(self, key: str):
        if key == "Enter":
            async for event in self.send_message():
                yield event

    # Session info
    sessions: list[Session] = []
    current_session_id: int = (
        0  # 0 or None indicates no session selected/new session needed
    )
    user_id: int = 1
    current_agent: str = "onboarding"

    # Delete session state
    confirm_dialog_open: bool = False
    session_to_delete: int | None = None

    def ask_delete_session(self, session_id: int):
        self.session_to_delete = session_id
        self.confirm_dialog_open = True

    def cancel_delete_session(self):
        self.confirm_dialog_open = False
        self.session_to_delete = None

    async def confirm_delete_session(self):
        if self.session_to_delete:
            with rx.session() as db_session:
                session = db_session.get(Session, self.session_to_delete)
                if session:
                    session.is_deleted = True
                    db_session.add(session)
                    db_session.commit()

            # Refresh list
            self.load_sessions()
            
            # If we deleted the current session, switch to another or new
            if self.current_session_id == self.session_to_delete:
                if self.sessions:
                    await self.select_session(self.sessions[0].id)
                else:
                    await self.create_new_session()
            
        self.confirm_dialog_open = False
        self.session_to_delete = None

    def load_sessions(self):
        """Load all sessions for the current user."""
        with rx.session() as session:
            self.sessions = session.exec(
                select(Session)
                .where(Session.user_id == self.user_id)
                .where(Session.is_deleted == False)
                .order_by(Session.updated_at.desc())
            ).all()
        # If no sessions, create one? Or wait for user.
        if self.sessions and self.current_session_id == 0:
            self.select_session(self.sessions[0].id)
        elif not self.sessions and self.current_session_id == 0:
            self.create_new_session()

    async def generate_title_for_session(self, session_id: int):
        """Generate a title for the session if it doesn't have one."""
        with rx.session() as db_session:
            session = db_session.get(Session, session_id)
            if not session or session.title:
                return

            yield
            # Get messages to summarize
            msgs = db_session.exec(
                select(Message)
                .where(Message.session_id == session_id)
                .order_by(Message.created_at)
            ).all()

            if not msgs:
                return

            # Simple summarization prompt
            # Limit to first 2000 chars to save tokens
            conversation_text = "\n".join([
                f"{m.sender}: {m.content_text}" for m in msgs
            ])
            if len(conversation_text) > 2000:
                conversation_text = conversation_text[:2000] + "..."

        try:
            orch = Orchestrator()
            # We can reuse an agent or ask orchestrator for a summarizer
            # For simplicity, we'll ask a generic agent or the current one (if stateless enough)
            # Actually, Orchestrator might not have a direct 'summarize' method.
            # We can just prompt the current agent type.

            # Ideally: orch.get_summarizer()...
            # Or just use the 'onboarding' agent for utility tasks?
            # Let's use the current agent loop or a new utility request.
            # "Please summarize this conversation in 3-5 words for a title."

            # We need to construct a prompt.
            # Since agents are chat-based, we can try to instantiate a temporary agent.
            # Assuming 'onboarding' is safe.
            temp_session = Session(
                session_id=session_id, user_id=self.user_id, session_type="onboarding"
            )
            agent = orch.get_agent_for_session(temp_session)

            summary_prompt = [
                {
                    "sender": "user",
                    "content_text": f"Summarize the following conversation into a short title (max 5 words). Return ONLY the title, no quotes.\n\n{conversation_text}",
                }
            ]
            title, _ = agent.get_response(
                summary_prompt
            )  # Unpack tuple, ignore metadata
            title = title.strip().strip('"')

            with rx.session() as db_session:
                session = db_session.get(Session, session_id)
                if session:
                    session.title = title
                    db_session.add(session)
                    db_session.commit()

            # Refresh sessions list to show new title
            self.load_sessions()
            yield

        except Exception as e:
            print(f"Failed to generate title: {e}")

    async def create_new_session(self, session_type: str = "onboarding"):
        """Create a new chat session."""
        if self.current_session_id:
            async for _ in self.generate_title_for_session(self.current_session_id):
                yield

        with rx.session() as db_session:
            new_session = Session(user_id=self.user_id, session_type=session_type)
            db_session.add(new_session)
            db_session.commit()
            db_session.refresh(new_session)
            self.current_session_id = new_session.id
            self.load_sessions()
            self.messages = []

    async def select_session(self, session_id: int):
        """Select a session and load its messages."""
        if self.current_session_id and self.current_session_id != session_id:
            async for _ in self.generate_title_for_session(self.current_session_id):
                yield

        self.current_session_id = session_id
        self.messages = []
        with rx.session() as db_session:
            msgs = db_session.exec(
                select(Message)
                .where(Message.session_id == session_id)
                .order_by(Message.created_at)
            ).all()
            for m in msgs:
                self.messages.append({
                    "sender": m.sender,
                    "content_text": m.content_text,
                    "created_at": m.created_at.strftime("%H:%M")
                    if m.created_at
                    else "",
                })
        # Scroll to bottom after loading
        async for _ in self.scroll_to_bottom():
            yield

    async def scroll_to_bottom(self):
        """Scroll to the bottom of the chat."""
        # Yield to let UI update first
        yield
        yield rx.call_script(
            "var el = document.getElementById('scroll-anchor'); if (el) el.scrollIntoView({ behavior: 'smooth' });"
        )

    async def send_message(self):
        if not self.input_text:
            return

        # Ensure we have a session
        if not self.current_session_id:
            self.create_new_session()

        # Store current text and clear input immediately
        current_text = self.input_text
        self.input_text = ""

        # Add user message
        timestamp = datetime.now().strftime("%H:%M")
        new_msg = {
            "sender": "user",
            "content_text": current_text,
            "created_at": timestamp,
        }
        self.messages.append(new_msg)

        # Process with Orchestrator
        self.is_processing = True
        yield
        yield rx.call_script(
            "var el = document.getElementById('scroll-anchor'); if (el) el.scrollIntoView({ behavior: 'smooth' });"
        )

        try:
            import time
            from ..models.token_usage import TokenUsage

            orch = Orchestrator()
            session = Session(
                id=self.current_session_id,
                user_id=self.user_id,
                session_type=self.current_agent,
            )
            agent = orch.get_agent_for_session(session)

            # Measure response time
            start_time = time.time()

            # Prepare kwargs for the agent (e.g. curriculum data for ProgressAgent)
            agent_kwargs = {}
            if self.current_agent == "progress_test":
                with rx.session() as db_session:
                    user = db_session.get(User, self.user_id)
                    cur = db_session.exec(
                        select(Curriculum).where(Curriculum.level == user.current_level)
                    ).first()
                    if cur:
                        agent_kwargs = {
                            "level": cur.level,
                            "chapter_title": cur.title,
                            "learning_goals": cur.learning_goals,
                            "common_pitfalls": cur.common_pitfalls,
                        }

            # Get response from LLM (streaming)
            ai_timestamp = datetime.now().strftime("%H:%M")
            ai_msg = {
                "sender": "agent",
                "content_text": "",
                "created_at": ai_timestamp,
            }
            self.messages.append(ai_msg)
            msg_index = len(self.messages) - 1

            usage_metadata = {}
            async for chunk_text, meta in agent.stream_response(
                self.messages[:-1], **agent_kwargs
            ):
                if chunk_text:
                    self.messages[msg_index]["content_text"] += chunk_text
                    # Trigger UI update
                    self.messages = list(self.messages)
                    yield
                if meta:
                    usage_metadata = meta

            # Save to DB
            with rx.session() as db_session:
                # Save messages
                user_message = Message(
                    session_id=self.current_session_id,
                    sender="user",
                    content_text=current_text,
                )
                db_session.add(user_message)
                db_session.flush()  # Get message ID

                agent_message = Message(
                    session_id=self.current_session_id,
                    sender="agent",
                    content_text=self.messages[msg_index]["content_text"],
                )
                db_session.add(agent_message)
                db_session.flush()  # Get message ID

                # Save token usage
                if usage_metadata:
                    token_usage = TokenUsage(
                        message_id=agent_message.id,
                        session_id=self.current_session_id,
                        user_id=self.user_id,
                        model_name=usage_metadata.get("model_name", "unknown"),
                        input_message=current_text,
                        output_message=self.messages[msg_index]["content_text"],
                        prompt_tokens=usage_metadata.get("prompt_tokens", 0),
                        completion_tokens=usage_metadata.get("completion_tokens", 0),
                        total_tokens=usage_metadata.get("total_tokens", 0),
                    )
                    db_session.add(token_usage)

                db_session.commit()

                # Update session updated_at
                session_obj = db_session.get(Session, self.current_session_id)
                if session_obj:
                    session_obj.updated_at = datetime.now()
                    db_session.add(session_obj)

                db_session.commit()

        except Exception as e:
            yield rx.toast.error(f"Error: {str(e)}")

        self.is_processing = False
        yield rx.call_script(
            "var el = document.getElementById('scroll-anchor'); if (el) el.scrollIntoView({ behavior: 'smooth' });"
        )

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if not self.is_recording:
            # Handle audio upload and processing
            pass
