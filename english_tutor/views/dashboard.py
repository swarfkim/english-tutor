import reflex as rx
import plotly.graph_objects as go
from .components import navbar, footer


def progress_chart():
    # Placeholder for a Plotly chart
    fig = go.Figure(
        data=go.Scatter(
            x=[1, 2, 3, 4],
            y=[10, 11, 12, 13],
            mode="lines+markers",
            name="Level Progress",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
    )
    return rx.plotly(data=fig, width="100%")


def dashboard_view() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Your Progress", size="8", margin_top="1em"),
                rx.hstack(
                    rx.card(
                        rx.vstack(
                            rx.text("Current Level", size="2", color_scheme="gray"),
                            rx.heading("Level 3", size="7", color_scheme="indigo"),
                            align_items="center",
                        ),
                        padding="2em",
                        width="100%",
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text("Recent Score", size="2", color_scheme="gray"),
                            rx.heading("85/100", size="7", color_scheme="green"),
                            align_items="center",
                        ),
                        padding="2em",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Learning Curve", size="5"),
                        progress_chart(),
                        width="100%",
                    ),
                    padding="2em",
                    width="100%",
                ),
                rx.heading("Recent Evaluations", size="5", margin_top="1em"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Date"),
                            rx.table.column_header_cell("Grammar"),
                            rx.table.column_header_cell("Pronunciation"),
                            rx.table.column_header_cell("Vocabulary"),
                            rx.table.column_header_cell("Fluency"),
                            rx.table.column_header_cell("Expression"),
                            rx.table.column_header_cell("Overall"),
                        ),
                    ),
                    rx.table.body(
                        rx.table.row(
                            rx.table.cell("2026-01-10"),
                            rx.table.cell(rx.badge("80", color_scheme="blue")),
                            rx.table.cell(rx.badge("75", color_scheme="blue")),
                            rx.table.cell(rx.badge("78", color_scheme="blue")),
                            rx.table.cell(rx.badge("82", color_scheme="green")),
                            rx.table.cell(rx.badge("76", color_scheme="blue")),
                            rx.table.cell(
                                rx.badge("78", color_scheme="green", variant="solid")
                            ),
                        ),
                        rx.table.row(
                            rx.table.cell("2026-01-12"),
                            rx.table.cell(rx.badge("88", color_scheme="green")),
                            rx.table.cell(rx.badge("82", color_scheme="green")),
                            rx.table.cell(rx.badge("85", color_scheme="green")),
                            rx.table.cell(rx.badge("90", color_scheme="green")),
                            rx.table.cell(rx.badge("84", color_scheme="green")),
                            rx.table.cell(
                                rx.badge("86", color_scheme="green", variant="solid")
                            ),
                        ),
                    ),
                    width="100%",
                    variant="surface",
                ),
                align_items="start",
                spacing="6",
                padding_y="2em",
            ),
        ),
        footer(),
        min_height="100vh",
    )
