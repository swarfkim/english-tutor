import reflex as rx
from .views.index import index
from .views.chat import chat_view
from .views.dashboard import dashboard_view
from .views.admin import admin_view
from .views.login import login_view
from .db_manager import DBManager

# Start DB Manager
DBManager.start()

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="indigo",
    )
)

app.add_page(index, route="/")
app.add_page(chat_view, route="/chat")
app.add_page(dashboard_view, route="/dashboard")
app.add_page(admin_view, route="/admin")
app.add_page(login_view, route="/login")
