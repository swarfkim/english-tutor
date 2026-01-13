import reflex as rx
from .components import navbar, footer


def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading(
                    "Master English with AI", size="9", weight="bold", margin_top="2em"
                ),
                rx.text(
                    "Personalized English tutoring powered by Multi-Agent AI and Gemini Audio API.",
                    size="5",
                    color_scheme="gray",
                    text_align="center",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "Get Started",
                            size="4",
                            color_scheme="indigo",
                            variant="solid",
                        ),
                        href="/chat",
                    ),
                    rx.link(rx.button("View Demo", size="4", variant="soft"), href="#"),
                    spacing="4",
                    margin_top="1em",
                ),
                rx.image(
                    src="/logo.png",
                    width="300px",
                    height="auto",
                    margin_top="3em",
                    border_radius="30px",
                    box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.5)",
                ),
                align_items="center",
                spacing="6",
                min_height="80vh",
            ),
        ),
        footer(),
        background="radial-gradient(circle at top right, #f0f4ff, #ffffff)",
        min_height="100vh",
    )
