# services.py
from .repositories import UserRepo

class UserService:
    def __init__(self):
        self.user_repo = UserRepo()

    def register_user(self, username: str, password: str, email: str):
        if not username or not password or not email:
            raise ValueError("All fields are required")

        if self.user_repo.user_exists(username):
            raise ValueError("User already exists")

        self.user_repo.create(username, password, email)

    def login_user(self, username: str, password: str):
        if not username or not password:
            raise ValueError("Username and password are required")

        if not self.user_repo.authenticate_user(username, password):
            raise ValueError("Incorrect username or password")

        # Here, you can add more logic like generating a token or managing sessions
            return True
