import reflex as rx
from .components import navbar, footer
from ..state.chat_state import ChatState
from ..models.user import Session


def chat_bubble(msg: dict[str, Any]) -> rx.Component:
    is_user = msg["sender"] == "user"

    # Heuristic for table content to allow wider width
    has_table = msg["content_text"].contains("|")
    max_w = rx.cond(has_table, "100%", "66%")

    return rx.hstack(
        rx.vstack(
            rx.box(
                rx.markdown(
                    msg["content_text"],
                    color=rx.cond(is_user, "white", "black"),
                    line_height="1.3",
                ),
                background=rx.cond(is_user, "#6366f1", "#e5e7eb"),
                padding_x="0.8em",
                padding_y="0.4em",
                border_radius="18px",
                border_bottom_right_radius=rx.cond(is_user, "0", "18px"),
                border_bottom_left_radius=rx.cond(is_user, "18px", "0"),
                max_width="100%",  # Box takes width of vstack, which is constrained by max_w logic if needed, but here we likely want text logic
                # Actually max_w logic from before:
                # max_w = rx.cond(has_table, "100%", "66%") applies to the BUBBLE.
                # So we apply max_w to this BOX (or the vstack if we want timestamp to wrap? No timestamp is short).
                # Let's apply max_w to the vstack to constrain the whole message block?
                # Or just the box? If box is constrained, vstack might be naturally constrained.
                # Let's keep max_w on the box as before.
                width="fit-content",
                position="relative",
                _after=rx.cond(
                    is_user,
                    {
                        "content": "''",
                        "position": "absolute",
                        "bottom": "0",
                        "right": "-6px",
                        "width": "0",
                        "height": "0",
                        "border_left": "10px solid #6366f1",
                        "border_bottom": "10px solid transparent",
                    },
                    {
                        "content": "''",
                        "position": "absolute",
                        "bottom": "0",
                        "left": "-6px",
                        "width": "0",
                        "height": "0",
                        "border_right": "10px solid #e5e7eb",
                        "border_bottom": "10px solid transparent",
                    },
                ),
            ),
            rx.text(
                msg["created_at"],
                font_size="0.65em",
                color="gray.500",
                margin_top="0.2em",
                align_self=rx.cond(is_user, "flex-end", "flex-start"),
            ),
            align_items=rx.cond(is_user, "end", "start"),
            spacing="1",
            max_width=max_w,  # Constrain the stack (bubble+time) width
        ),
        justify=rx.cond(is_user, "end", "start"),
        width="100%",
        padding_bottom="0.5em",
    )


def sidebar_item(session: Session) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("message-square", size=16),
            rx.text(
                rx.cond(session.title, session.title, f"Session {session.id}"),
                font_size="sm",
                truncate=True,
                max_width="150px",
            ),
            rx.spacer(),
            rx.text(
                rx.cond(
                    session.created_at,
                    session.created_at.to(str).split("T")[0],  # Simple YYYY-MM-DD
                    "",
                ),
                font_size="xs",
                color="gray.400",
            ),
            width="100%",
            align_items="center",
            spacing="2",
        ),
        padding="0.75em",
        border_radius="8px",
        cursor="pointer",
        background=rx.cond(
            session.id == ChatState.current_session_id,
            "rgba(99, 102, 241, 0.1)",  # Indigo tint
            "transparent",
        ),
        color=rx.cond(
            session.id == ChatState.current_session_id,
            "indigo",
            "gray.700",
        ),
        _hover={"background": "gray.100"},
        on_click=lambda: ChatState.select_session(session.id),
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Your Chats",
            size="4",
            weight="bold",
            color="gray.700",
            padding_bottom="1em",
        ),
        rx.button(
            rx.icon("plus", size=16),
            "New Chat",
            width="100%",
            variant="solid",
            color_scheme="indigo",
            radius="full",
            on_click=ChatState.create_new_session,
        ),
        rx.divider(),
        rx.vstack(
            rx.foreach(ChatState.sessions, sidebar_item),
            width="100%",
            spacing="1",
            overflow_y="auto",
            padding_right="0.5em",  # subtle spacing for scrollbar
        ),
        width="280px",  # Slightly wider
        height="100%",
        padding="1.5em",
        border_right="1px solid #f3f4f6",
        background="gray.50",
        display=["none", "none", "flex"],
    )


def chat_view() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.box(
                rx.hstack(
                    sidebar(),
                    rx.container(
                        rx.vstack(
                            rx.box(
                                rx.heading(
                                    "English Tutoring Session",
                                    size="6",
                                    color="gray.800",
                                ),
                                rx.text(
                                    "AI-powered language learning",
                                    size="2",
                                    color="gray.500",
                                ),
                                text_align="center",
                                width="100%",
                                margin_top="1em",
                                margin_bottom="1em",
                            ),
                            rx.divider(),
                            rx.scroll_area(
                                rx.vstack(
                                    rx.foreach(ChatState.messages, chat_bubble),
                                    rx.cond(
                                        ChatState.is_processing,
                                        rx.hstack(
                                            rx.spinner(size="2", color="indigo"),
                                            rx.text(
                                                "Agent is typing...",
                                                color="gray.500",
                                                font_size="sm",
                                            ),
                                            spacing="2",
                                            padding="1em",
                                        ),
                                    ),
                                    rx.box(id="scroll-anchor", height="1px"),
                                    width="100%",
                                    spacing="4",
                                    padding="1em",
                                ),
                                height="100%",
                                width="100%",
                                scrollbars="vertical",
                                type="hover",
                            ),
                            rx.hstack(
                                rx.input(
                                    placeholder="Type your message...",
                                    value=ChatState.input_text,
                                    on_change=ChatState.set_input_text,
                                    on_key_down=ChatState.handle_key,
                                    disabled=ChatState.is_processing,
                                    width="100%",
                                    variant="soft",
                                    color_scheme="gray",
                                    radius="full",
                                    padding_x="1.5em",
                                ),
                                rx.button(
                                    rx.icon("mic", size=20),
                                    color_scheme=rx.cond(
                                        ChatState.is_recording, "red", "gray"
                                    ),
                                    variant="ghost",
                                    on_click=ChatState.toggle_recording,
                                    disabled=ChatState.is_processing,
                                    radius="full",
                                ),
                                rx.button(
                                    rx.text("Send", weight="bold"),
                                    rx.icon("send", size=18),
                                    background="indigo",
                                    color="white",
                                    _hover={
                                        "background": "indigo.600",
                                        "transform": "scale(1.05)",
                                    },
                                    transition="all 0.2s",
                                    on_click=ChatState.send_message,
                                    loading=ChatState.is_processing,
                                    disabled=ChatState.is_processing,
                                    radius="full",
                                    padding_x="1.5em",
                                ),
                                width="100%",
                                spacing="3",
                                padding_y="1em",
                                padding_x="0.5em",
                                background="gray.50",
                                border_radius="full",
                                border="1px solid #f3f4f6",
                            ),
                            align_items="center",
                            width="100%",
                            height="100%",
                        ),
                        padding="0",
                        height="100%",
                        max_width="100%",
                        flex="1",
                    ),
                    width="100%",
                    height="100%",
                    spacing="0",
                ),
                width=["100%", "95%", "1200px"],
                height="85vh",
                background="white",
                border_radius="30px",
                box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                overflow="hidden",
                border="1px solid #e5e7eb",
            ),
            width="100%",
            height="calc(100vh - 80px)",
            padding="1em",
        ),
        footer(),
        min_height="100vh",
        background="#F3F4F6",
        font_family="Inter, sans-serif",
        on_mount=ChatState.load_sessions,
    )
