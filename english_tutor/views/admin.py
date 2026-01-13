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


def admin_view() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Admin Dashboard", size="8", margin_top="1em"),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Users", value="users"),
                        rx.tabs.trigger("Prompts", value="prompts"),
                        rx.tabs.trigger("Tokens", value="tokens"),
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            rx.heading("User Management", size="5", margin_top="1em"),
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("User"),
                                        rx.table.column_header_cell("Status"),
                                        rx.table.column_header_cell("Role"),
                                        rx.table.column_header_cell("Action"),
                                    ),
                                ),
                                rx.table.body(
                                    rx.table.row(
                                        rx.table.cell("user_one"),
                                        rx.table.cell("Active", color_scheme="green"),
                                        rx.table.cell("User"),
                                        rx.table.cell(
                                            rx.button(
                                                "Disable", size="1", color_scheme="red"
                                            )
                                        ),
                                    ),
                                    rx.table.row(
                                        rx.table.cell("admin_user"),
                                        rx.table.cell("Active", color_scheme="green"),
                                        rx.table.cell("Admin"),
                                        rx.table.cell(
                                            rx.button(
                                                "Disable", size="1", color_scheme="red"
                                            )
                                        ),
                                    ),
                                ),
                                width="100%",
                            ),
                            width="100%",
                        ),
                        value="users",
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            rx.heading("Prompt Management", size="5", margin_top="1em"),
                            rx.text(
                                "Edit system prompts for each agent.", color="gray"
                            ),
                            rx.select(
                                ["Counselor", "Evaluator", "Tutor", "Planner"],
                                placeholder="Select Agent",
                                on_change=AdminState.set_selected_agent,
                                value=AdminState.selected_agent,
                            ),
                            rx.cond(
                                AdminState.selected_agent != "",
                                rx.vstack(
                                    rx.heading(
                                        "Current Prompt", size="4", margin_top="1em"
                                    ),
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
                                    rx.dialog.root(
                                        rx.dialog.content(
                                            rx.vstack(
                                                rx.dialog.title("AI Prompt Optimizer"),
                                                rx.dialog.description(
                                                    "Describe how you want to improve the prompt. AI will suggest a new version."
                                                ),
                                                rx.scroll_area(
                                                    rx.vstack(
                                                        rx.foreach(
                                                            AdminState.optimizer_history,
                                                            lambda msg: rx.box(
                                                                rx.vstack(
                                                                    rx.text(
                                                                        msg[
                                                                            "role"
                                                                        ].upper(),
                                                                        size="1",
                                                                        weight="bold",
                                                                        color=rx.cond(
                                                                            msg["role"]
                                                                            == "user",
                                                                            "blue",
                                                                            "green",
                                                                        ),
                                                                    ),
                                                                    rx.text(
                                                                        msg["content"],
                                                                        size="2",
                                                                    ),
                                                                    rx.cond(
                                                                        msg["role"]
                                                                        == "agent",
                                                                        rx.button(
                                                                            "Apply this version",
                                                                            size="1",
                                                                            variant="soft",
                                                                            color_scheme="green",
                                                                            on_click=lambda: (
                                                                                AdminState.apply_optimized_prompt(
                                                                                    msg[
                                                                                        "content"
                                                                                    ]
                                                                                )
                                                                            ),
                                                                        ),
                                                                    ),
                                                                    align_items="start",
                                                                    spacing="1",
                                                                ),
                                                                padding="0.8em",
                                                                background=rx.cond(
                                                                    msg["role"]
                                                                    == "user",
                                                                    "#f0f7ff",
                                                                    "#f0fff4",
                                                                ),
                                                                border_radius="10px",
                                                                width="100%",
                                                            ),
                                                        ),
                                                        spacing="3",
                                                        width="100%",
                                                    ),
                                                    height="350px",
                                                    width="100%",
                                                    padding_y="1em",
                                                ),
                                                rx.hstack(
                                                    rx.input(
                                                        placeholder="e.g. Make it more encouraging for beginners...",
                                                        value=AdminState.optimizer_input,
                                                        on_change=AdminState.set_optimizer_input,
                                                        width="100%",
                                                    ),
                                                    rx.button(
                                                        "Generate",
                                                        on_click=AdminState.optimize_prompt,
                                                        loading=AdminState.is_optimizing,
                                                        color_scheme="indigo",
                                                    ),
                                                    width="100%",
                                                ),
                                                rx.hstack(
                                                    rx.dialog.close(
                                                        rx.button(
                                                            "Cancel",
                                                            variant="soft",
                                                            color_scheme="gray",
                                                        )
                                                    ),
                                                    justify="end",
                                                    width="100%",
                                                ),
                                                spacing="4",
                                                width="100%",
                                            ),
                                            max_width="600px",
                                        ),
                                        open=AdminState.show_optimizer,
                                    ),
                                    rx.divider(margin_y="2em"),
                                    rx.heading("Version History", size="4"),
                                    rx.scroll_area(
                                        rx.vstack(
                                            rx.foreach(
                                                AdminState.prompt_history,
                                                prompt_history_item,
                                            ),
                                            width="100%",
                                            spacing="2",
                                        ),
                                        height="400px",
                                        scrollbars="vertical",
                                    ),
                                    width="100%",
                                    spacing="3",
                                ),
                            ),
                            width="100%",
                        ),
                        value="prompts",
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            rx.heading(
                                "Token Usage Analytics", size="5", margin_top="1em"
                            ),
                            rx.hstack(
                                rx.card(
                                    rx.vstack(
                                        rx.text("Total Tokens", size="2", color="gray"),
                                        rx.heading(
                                            AdminState.total_tokens.to(str),
                                            size="6",
                                            color="indigo",
                                        ),
                                        align_items="center",
                                    ),
                                    padding="1.5em",
                                ),
                                rx.card(
                                    rx.vstack(
                                        rx.text(
                                            "Estimated Cost", size="2", color="gray"
                                        ),
                                        rx.heading(
                                            f"${AdminState.total_cost:.4f}",
                                            size="6",
                                            color="green",
                                        ),
                                        align_items="center",
                                    ),
                                    padding="1.5em",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                            rx.button(
                                "Refresh Data",
                                on_click=AdminState.load_token_usage,
                                color_scheme="indigo",
                                variant="soft",
                            ),
                            rx.heading("Recent Messages", size="4", margin_top="2em"),
                            rx.scroll_area(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Time"),
                                            rx.table.column_header_cell("Model"),
                                            rx.table.column_header_cell("Input"),
                                            rx.table.column_header_cell("Output"),
                                            rx.table.column_header_cell(
                                                "Prompt Tokens"
                                            ),
                                            rx.table.column_header_cell("Completion"),
                                            rx.table.column_header_cell("Cached"),
                                            rx.table.column_header_cell("Total"),
                                            rx.table.column_header_cell("Time (ms)"),
                                        ),
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            AdminState.token_usage_records,
                                            lambda record: rx.table.row(
                                                rx.table.cell(
                                                    record.created_at.to(str)
                                                ),
                                                rx.table.cell(
                                                    rx.badge(
                                                        record.model_name, size="1"
                                                    )
                                                ),
                                                rx.table.cell(
                                                    rx.cond(
                                                        record.input_message.length()
                                                        > 50,
                                                        record.input_message[:50]
                                                        + "...",
                                                        record.input_message,
                                                    ),
                                                    max_width="200px",
                                                    truncate=True,
                                                ),
                                                rx.table.cell(
                                                    rx.cond(
                                                        record.output_message.length()
                                                        > 50,
                                                        record.output_message[:50]
                                                        + "...",
                                                        record.output_message,
                                                    ),
                                                    max_width="200px",
                                                    truncate=True,
                                                ),
                                                rx.table.cell(
                                                    record.prompt_tokens.to(str)
                                                ),
                                                rx.table.cell(
                                                    record.completion_tokens.to(str)
                                                ),
                                                rx.table.cell(
                                                    record.cached_prompt_tokens.to(str)
                                                ),
                                                rx.table.cell(
                                                    rx.badge(
                                                        record.total_tokens.to(str),
                                                        color_scheme="indigo",
                                                    )
                                                ),
                                                rx.table.cell(
                                                    record.response_time_ms.to(str)
                                                ),
                                            ),
                                        ),
                                    ),
                                    width="100%",
                                    variant="surface",
                                ),
                                height="500px",
                                scrollbars="both",
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        value="tokens",
                    ),
                    width="100%",
                ),
                align_items="start",
                spacing="6",
                padding_y="2em",
            ),
        ),
        footer(),
        min_height="100vh",
    )
