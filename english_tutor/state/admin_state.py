import reflex as rx

from sqlmodel import select, func
from ..models.content import AgentPrompt
from ..models.token_usage import TokenUsage


class AdminState(rx.State):
    """State for admin dashboard."""

    # Prompt management
    selected_agent: str = ""
    current_prompt_text: str = ""
    original_prompt_text: str = ""  # Track loaded state for change detection
    prompt_history: list[AgentPrompt] = []

    # Prompt Optimizer State
    show_optimizer: bool = False
    optimizer_history: list[
        dict[str, str]
    ] = []  # [{"role": "user", "content": "..."}, {"role": "agent", "content": "..."}]
    optimizer_input: str = ""
    is_optimizing: bool = False

    # Token usage tracking
    token_usage_records: list[TokenUsage] = []
    total_tokens: int = 0
    total_cost: float = 0.0

    def load_token_usage(self):
        """Load recent token usage records."""
        with rx.session() as session:
            records = session.exec(
                select(TokenUsage).order_by(TokenUsage.created_at.desc()).limit(100)
            ).all()

            self.token_usage_records = list(records)

            # Calculate totals
            total = session.exec(select(func.sum(TokenUsage.total_tokens))).first()

            self.total_tokens = total or 0

            # Estimate cost (example: $0.001 per 1000 tokens)
            self.total_cost = (self.total_tokens / 1000) * 0.001

    # Mapping between UI labels and internal keys/file paths
    AGENT_CONFIG = {
        "Counselor": {
            "key": "onboarding",
            "path": "english_tutor/prompts/counselor.txt",
        },
        "Evaluator": {
            "key": "evaluation",
            "path": "english_tutor/prompts/evaluator.txt",
        },
        "Tutor": {"key": "tutoring", "path": "english_tutor/prompts/tutor.txt"},
        "Planner": {"key": "planning", "path": "english_tutor/prompts/planner.txt"},
    }

    def set_selected_agent(self, agent_name: str):
        """Set the selected agent and load its current prompt."""
        self.selected_agent = agent_name
        self.load_current_prompt()
        self.load_prompt_history()

    def load_current_prompt(self):
        """Load the active prompt for the selected agent."""
        if not self.selected_agent:
            return

        config = self.AGENT_CONFIG.get(self.selected_agent)
        if not config:
            return

        agent_key = config["key"]

        with rx.session() as session:
            prompt = session.exec(
                select(AgentPrompt)
                .where(AgentPrompt.agent_name == agent_key)
                .where(AgentPrompt.is_active == True)
                .order_by(AgentPrompt.version.desc())
            ).first()

            if prompt:
                self.current_prompt_text = prompt.prompt_text
                self.original_prompt_text = prompt.prompt_text
            else:
                # Fallback to file if empty in DB
                try:
                    with open(config["path"], "r") as f:
                        text = f.read()
                        self.current_prompt_text = text
                        self.original_prompt_text = text
                except Exception as e:
                    print(f"Failed to load default prompt from {config['path']}: {e}")
                    self.current_prompt_text = ""
                    self.original_prompt_text = ""

    def load_prompt_history(self):
        """Load all versions of prompts for the selected agent."""
        if not self.selected_agent:
            return

        config = self.AGENT_CONFIG.get(self.selected_agent)
        if not config:
            return

        agent_key = config["key"]

        with rx.session() as session:
            prompts = session.exec(
                select(AgentPrompt)
                .where(AgentPrompt.agent_name == agent_key)
                .order_by(AgentPrompt.version.desc())
            ).all()

            self.prompt_history = list(prompts)

    def set_prompt_text(self, text: str):
        """Update the current prompt text being edited."""
        self.current_prompt_text = text

    def save_prompt(self):
        """Save the current prompt as a new version."""
        if not self.selected_agent or not self.current_prompt_text:
            return

        config = self.AGENT_CONFIG.get(self.selected_agent)
        if not config:
            return

        agent_key = config["key"]

        with rx.session() as session:
            # Deactivate all previous versions
            old_prompts = session.exec(
                select(AgentPrompt)
                .where(AgentPrompt.agent_name == agent_key)
                .where(AgentPrompt.is_active == True)
            ).all()

            for old_prompt in old_prompts:
                old_prompt.is_active = False
                session.add(old_prompt)

            # Get the next version number
            max_version = session.exec(
                select(AgentPrompt.version)
                .where(AgentPrompt.agent_name == agent_key)
                .order_by(AgentPrompt.version.desc())
            ).first()

            next_version = (max_version or 0) + 1

            # Create new prompt version
            new_prompt = AgentPrompt(
                agent_name=agent_key,
                prompt_text=self.current_prompt_text,
                version=next_version,
                is_active=True,
            )

            session.add(new_prompt)
            session.commit()

        # Reload history
        self.load_prompt_history()

        return rx.toast.success(f"Saved {self.selected_agent} prompt v{next_version}")

    def restore_version(self, version: int):
        """Restore a previous version as the active prompt."""
        if not self.selected_agent:
            return

        config = self.AGENT_CONFIG.get(self.selected_agent)
        if not config:
            return

        agent_key = config["key"]

        with rx.session() as session:
            # Deactivate all versions
            all_prompts = session.exec(
                select(AgentPrompt).where(AgentPrompt.agent_name == agent_key)
            ).all()

            for prompt in all_prompts:
                prompt.is_active = prompt.version == version
                session.add(prompt)

            session.commit()

        # Reload
        self.load_current_prompt()
        self.load_prompt_history()

        return rx.toast.success(f"Restored version {version}")

    @rx.var
    def has_changes(self) -> bool:
        return self.current_prompt_text != self.original_prompt_text

    def set_optimizer_input(self, text: str):
        self.optimizer_input = text

    def reset_prompt(self):
        """Reset current prompt to its original state."""
        self.current_prompt_text = self.original_prompt_text

    def toggle_optimizer(self):
        """Toggle the optimizer modal."""
        self.show_optimizer = not self.show_optimizer
        if self.show_optimizer:
            self.optimizer_history = []
            self.optimizer_input = ""

    async def optimize_prompt(self):
        """Send requirements to AI to optimize the prompt."""
        if not self.optimizer_input:
            return

        user_req = self.optimizer_input
        self.optimizer_input = ""
        self.optimizer_history.append({"role": "user", "content": user_req})
        self.is_optimizing = True
        yield

        try:
            from ..agents.orchestrator import Orchestrator
            from ..models.user import Session

            orch = Orchestrator()

            # Use onboarding agent for meta-prompting tasks
            temp_session = Session(id=0, user_id=0, session_type="onboarding")
            agent = orch.get_agent_for_session(temp_session)

            system_meta_prompt = f"""You are a Prompt Engineering Expert. 
Your task is to help the user improve an LLM system prompt for an English Tutoring app.

Current Prompt to improve:
---
{self.current_prompt_text}
---

The goal for improvement is: {user_req}

Please provide an improved version of the prompt. 
IMPORTANT: Return the FULL improved prompt text clearly in your response. 
Keep it professional and effective.
Response only with the improved prompt content or very brief explanation."""

            messages = [{"sender": "user", "content_text": system_meta_prompt}]

            response_text, _ = agent.get_response(messages)

            self.optimizer_history.append({"role": "agent", "content": response_text})
        except Exception as e:
            yield rx.toast.error(f"Optimization failed: {str(e)}")
        finally:
            self.is_optimizing = False

    def apply_optimized_prompt(self, text: str):
        """Apply the suggested prompt to the main text area."""
        self.current_prompt_text = text
        self.show_optimizer = False
        return rx.toast.success("AI suggested prompt applied!")
