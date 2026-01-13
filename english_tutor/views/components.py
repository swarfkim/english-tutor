import reflex as rx


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(
                    src="/logo.png", width="40px", height="auto", border_radius="10px"
                ),
                rx.heading(
                    "AI English Tutor",
                    size="6",
                    weight="bold",
                    color_gradient=rx.color("indigo", 9),
                ),
                spacing="3",
                align_items="center",
            ),
            rx.hstack(
                rx.link("Dashboard", href="/dashboard", color_scheme="gray"),
                rx.link("Chat", href="/chat", color_scheme="gray"),
                rx.link("Admin", href="/admin", color_scheme="gray"),
                rx.button("Logout", variant="soft", color_scheme="indigo"),
                spacing="6",
                align_items="center",
            ),
            justify="between",
            padding_x="4em",
            padding_y="1em",
            background="rgba(255, 255, 255, 0.8)",
            backdrop_filter="blur(10px)",
            border_bottom="1px solid rgba(0,0,0,0.1)",
            position="sticky",
            top="0",
            z_index="100",
            width="100%",
        )
    )


def footer() -> rx.Component:
    return rx.box(
        rx.center(
            rx.text(
                "© 2026 AI English Tutor. All rights reserved.",
                size="2",
                color_scheme="gray",
            ),
            width="100%",
        ),
        padding_y="1.5em",
        width="100%",
        background="rgba(255, 255, 255, 0.8)",
        backdrop_filter="blur(10px)",
        border_top="1px solid rgba(0,0,0,0.1)",
        position="sticky",
        bottom="0",
        z_index="50",
    )
