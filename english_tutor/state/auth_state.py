import reflex as rx
from ..models.user import User


class AuthState(rx.State):
    """Handle user authentication."""

    username: str = ""
    password: str = ""
    is_authenticated: bool = False
    error_message: str = ""

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password

    def login(self):
        with rx.session() as session:
            user = session.exec(
                User.select.where(User.username == self.username)
            ).first()
            if user and user.password_hash == self.password:  # Simple check for now
                self.is_authenticated = True
                self.error_message = ""
                return rx.redirect("/chat")
            else:
                self.error_message = "Invalid username or password"

    def signup(self):
        with rx.session() as session:
            existing = session.exec(
                User.select.where(User.username == self.username)
            ).first()
            if existing:
                self.error_message = "Username already exists"
                return

            new_user = User(username=self.username, password_hash=self.password)
            session.add(new_user)
            session.commit()
            self.is_authenticated = True
            return rx.redirect("/chat")

    def logout(self):
        self.is_authenticated = False
        return rx.redirect("/")
