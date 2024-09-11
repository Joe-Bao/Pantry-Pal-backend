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
    
    def user_exists(self, username: str) -> bool:
        for user in self.users:
            if user.username == username:
                return True
        return False
    
    def create(self, username: str, password: str, email: str, birthday: str):
        self.users.append(User(username, password, email, birthday))

    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.get(username)
        return check_password_hash(user.password, password)


class ShoppingList:
    def __init__(self, name: str):
        self.name = name

class ShoppingListRepo:
    lists: List[ShoppingList] = []

    def get(self, name: str) -> List:
        for l in self.lists:
            if l.name == name:
                return l
        raise Exception("List not found")
    
    def list_exists(self, name: str) -> bool:
        for l in self.lists:
            if l.name == name:
                return True
        return False
    
    def create(self, name: str):
        self.lists.append(List(name))

    def change_name(self, name: str, new_name: str):
        for l in self.lists:
            if l.name == name:
                l.name = new_name
                return
        raise Exception("List not found")

    def delete(self, name: str):
        for l in self.lists:
            if l.name == name:
                self.lists.remove(l)
                return
        raise Exception("List not found")

