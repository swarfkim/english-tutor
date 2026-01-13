import reflex as rx
from .components import navbar, footer
from ..state.auth_state import AuthState


def login_view() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("Login to Your Tutor", size="7"),
                rx.input(
                    placeholder="Username",
                    value=AuthState.username,
                    on_change=AuthState.set_username,
                    width="100%",
                ),
                rx.input(
                    placeholder="Password",
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                    width="100%",
                ),
                rx.button(
                    "Login",
                    on_click=AuthState.login,
                    width="100%",
                    color_scheme="indigo",
                ),
                rx.button(
                    "Sign Up", on_click=AuthState.signup, width="100%", variant="soft"
                ),
                rx.text(AuthState.error_message, color="red"),
                spacing="4",
                padding="3em",
                border="1px solid #e5e7eb",
                border_radius="15px",
                background="white",
                box_shadow="lg",
                width="400px",
            ),
            min_height="80vh",
        ),
        footer(),
        background="radial-gradient(circle at top right, #f0f4ff, #ffffff)",
        min_height="100vh",
    )
