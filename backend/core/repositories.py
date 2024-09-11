from typing import List
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username: str, password: str, email: str, birthday: str):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.birthday = birthday
        self.allergies = []
        self.diets = []
        self.intolerances = []
class UserRepo:
    users: List[User] = []


    def get(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        raise Exception("User not found")

