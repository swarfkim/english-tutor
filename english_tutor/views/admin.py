import reflex as rx
from .components import navbar, footer
from ..state.admin_state import AdminState


def prompt_history_item(prompt) -> rx.Component:
    """Display a single prompt version in the history."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.badge(f"v{prompt.version}", color_scheme="indigo"),
                    rx.cond(
                        prompt.is_active,
                        rx.badge("Active", color_scheme="green", variant="solid"),
                    ),
                    spacing="2",
                ),
                rx.text(
                    rx.cond(
                        prompt.prompt_text.length() > 100,
                        prompt.prompt_text[:100] + "...",
                        prompt.prompt_text,
                    ),
                    size="2",
                    color="gray",
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            rx.button(
                "Restore",
                size="1",
                variant="soft",
                on_click=lambda: AdminState.restore_version(prompt.version),
                disabled=prompt.is_active,
            ),
            width="100%",
            justify="between",
            align_items="start",
        ),
        padding="1em",
        border="1px solid #e5e7eb",
        border_radius="8px",
        width="100%",
    )


def agent_selector() -> rx.Component:
    return rx.vstack(
        rx.text("Edit system prompts for each agent.", color="gray"),
        rx.select(
            ["Counselor", "Evaluator", "Tutor", "Planner", "Placement", "Progress"],
            placeholder="Select Agent",
            on_change=AdminState.set_selected_agent,
            value=AdminState.selected_agent,
        ),
        width="100%",
        spacing="2",
    )


def prompt_editor() -> rx.Component:
    return rx.cond(
        AdminState.selected_agent != "",
        rx.vstack(
            rx.heading("Current Prompt", size="4", margin_top="1em"),
            rx.text_area(
                value=AdminState.current_prompt_text,
                on_change=AdminState.set_prompt_text,
                placeholder="Prompt text...",
                width="100%",
                height="300px",
            ),
            rx.hstack(
                rx.button(
                    "Save as New Version",
                    color_scheme="indigo",
                    on_click=AdminState.save_prompt,
                    disabled=~AdminState.has_changes,
                ),
                rx.button(
                    "Reset",
                    color_scheme="gray",
                    variant="soft",
                    on_click=AdminState.reset_prompt,
                    disabled=~AdminState.has_changes,
                ),
                rx.button(
                    "Improve with AI",
                    rx.icon("sparkles", size=18),
                    color_scheme="purple",
                    variant="surface",
                    on_click=AdminState.toggle_optimizer,
                ),
                spacing="3",
            ),
            # AI Optimizer Modal included here for context
            rx.dialog.root(
                rx.dialog.content(
                    rx.vstack(
                        rx.dialog.title("AI Prompt Optimizer"),
                        rx.scroll_area(
                            rx.vstack(
                                rx.foreach(
                                    AdminState.optimizer_history,
                                    lambda msg: rx.box(
                                        rx.text(msg["content"], size="2"),
                                        padding="0.8em",
                                        background=rx.cond(
                                            msg["role"] == "user", "#f0f7ff", "#f0fff4"
                                        ),
                                        border_radius="10px",
                                        width="100%",
                                    ),
                                ),
                                spacing="2",
                            ),
                            height="300px",
                        ),
                        rx.input(
                            placeholder="Improvement requirements...",
                            value=AdminState.optimizer_input,
                            on_change=AdminState.set_optimizer_input,
                        ),
                        rx.hstack(
                            rx.button(
                                "Generate",
                                on_click=AdminState.optimize_prompt,
                                loading=AdminState.is_optimizing,
                            ),
                            rx.dialog.close(rx.button("Close", variant="soft")),
                        ),
                    ),
                ),
                open=AdminState.show_optimizer,
            ),
            width="100%",
            spacing="3",
        ),
    )


def token_stats() -> rx.Component:
    return rx.hstack(
        rx.card(
            rx.vstack(rx.text("Total Tokens"), rx.heading(AdminState.total_tokens))
        ),
        rx.card(
            rx.vstack(
                rx.text("Estimated Cost"), rx.heading(f"${AdminState.total_cost:.4f}")
            )
        ),
        width="100%",
        spacing="3",
    )


def usage_table() -> rx.Component:
    return rx.scroll_area(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Time"),
                    rx.table.column_header_cell("Model"),
                    rx.table.column_header_cell("Tokens"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    AdminState.token_usage_records,
                    lambda r: rx.table.row(
                        rx.table.cell(r.created_at.to(str)),
                        rx.table.cell(r.model_name),
                        rx.table.cell(r.total_tokens),
                    ),
                )
            ),
        ),
        height="400px",
    )


def curriculum_tab() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.heading("Levels", size="4"),
            rx.vstack(
                rx.foreach(
                    rx.Var.range(1, 9),
                    lambda lvl: rx.button(
                        f"Level {lvl}",
                        variant="ghost",
                        on_click=lambda: AdminState.select_curriculum_level(lvl),
                        background=rx.cond(
                            AdminState.selected_level == lvl,
                            "rgba(99, 102, 241, 0.1)",
                            "transparent",
                        ),
                        width="200px",
                        justify_content="start",
                    ),
                ),
                spacing="1",
            ),
            width="220px",
            border_right="1px solid #eee",
        ),
        rx.vstack(
            rx.heading(f"Level {AdminState.selected_level} Curriculum", size="5"),
            rx.text("Title"),
            rx.input(
                value=AdminState.curriculum_title,
                on_change=lambda v: AdminState.set_curriculum_field("title", v),
                width="100%",
            ),
            rx.text("Description"),
            rx.input(
                value=AdminState.curriculum_description,
                on_change=lambda v: AdminState.set_curriculum_field("description", v),
                width="100%",
            ),
            rx.text("Goals"),
            rx.text_area(
                value=AdminState.curriculum_learning_goals,
                on_change=lambda v: AdminState.set_curriculum_field("goals", v),
                width="100%",
            ),
            rx.text("Common Pitfalls"),
            rx.text_area(
                value=AdminState.curriculum_common_pitfalls,
                on_change=lambda v: AdminState.set_curriculum_field("pitfalls", v),
                width="100%",
            ),
            rx.text("Base Content"),
            rx.text_area(
                value=AdminState.curriculum_base_content,
                on_change=lambda v: AdminState.set_curriculum_field("content", v),
                width="100%",
                height="250px",
            ),
            rx.button(
                "Save Changes",
                on_click=AdminState.save_curriculum,
                color_scheme="indigo",
            ),
            width="100%",
            padding="1em",
            spacing="3",
            align_items="start",
        ),
        width="100%",
        align_items="start",
    )


@rx.page(route="/admin", title="Admin Dashboard")
def admin_view() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Admin Dashboard", size="8", margin_bottom="1em"),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Prompts", value="prompts"),
                        rx.tabs.trigger("Curriculum", value="curriculum"),
                        rx.tabs.trigger("Usage", value="usage"),
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            agent_selector(),
                            rx.divider(),
                            prompt_editor(),
                            rx.divider(),
                            rx.heading("History", size="4"),
                            rx.foreach(AdminState.prompt_history, prompt_history_item),
                            width="100%",
                            spacing="4",
                        ),
                        value="prompts",
                    ),
                    rx.tabs.content(curriculum_tab(), value="curriculum"),
                    rx.tabs.content(
                        rx.vstack(
                            token_stats(), rx.divider(), usage_table(), width="100%"
                        ),
                        value="usage",
                    ),
                    default_value="prompts",
                ),
                width="100%",
                padding_y="2em",
            )
        ),
        on_mount=[
            AdminState.load_prompt_history,
            AdminState.load_token_usage,
            AdminState.load_curriculums,
        ],
    )
