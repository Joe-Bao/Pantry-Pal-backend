from abc import abstractmethod
from typing import List, Dict
from werkzeug.security import generate_password_hash, check_password_hash
from utils import GetCurrentTimeInSeconds
from globals import DB_PREFIX_USER, DB_PREFIX_SHOPPING_LIST
from nanoid import generate

class GenericModel:
    def __init__(self, PK, SK):
        now = GetCurrentTimeInSeconds()
        self.PK = PK
        self.SK = SK
        self.createdAt = now
        self.modifiedAt = now

class GenenericRepo:
    @abstractmethod
    def get(self, PK: str, SK: str):
        pass

    @abstractmethod
    def delete(self, PK: str, SK: str):
        pass


class User(GenericModel):
    def __init__(self, username: str, password: str, email: str, birthday: str):
        id = generate()
        super().__init__(DB_PREFIX_USER + id, DB_PREFIX_USER + id)
        
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.birthday = birthday
        self.allergies = []
        self.diets = []
        self.intolerances = []


class UserRepo(GenenericRepo):
    users: Dict[str, User] = {}

    def get(self, id: str) -> User:
        user = self.users[DB_PREFIX_USER + id]
        if user is not None:
            return user
        raise Exception("User not found")
    
    def get_by_username(self, username: str) -> User:
        for user in self.users.values():
            if user.username == username:
                return user
        raise Exception("User not found")
    
    def user_exists(self, id: str) -> bool:
        user = self.users[DB_PREFIX_USER + id]
        if user is not None:
            return True
        return False
    
    def username_exists(self, username: str) -> bool:
        for user in self.users.values():
            if user.username == username:
                return True
        return False
    
    def create(self, username: str, password: str, email: str, birthday: str):
        user = User(username, password, email, birthday)
        self.users[user.PK] = user

    def authenticate_user(self, username: str, password: str) -> bool:
        user = self.get_by_username(username)
        return check_password_hash(user.password, password)


class ShoppingList(GenericModel):
    def __init__(self, userid: str, name: str):
        super().__init__(DB_PREFIX_USER + userid, DB_PREFIX_SHOPPING_LIST + generate())
        
        self.name = name

class ShoppingListRepo(GenenericRepo):
    lists: List[ShoppingList] = []

    def get(self, uid: str, lid: str) -> List:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST + lid
        for l in self.lists:
            if l.PK == PK and l.SK == SK:
                return l
        raise Exception("List not found")
    
    def list_exists(self, uid: str, lid: str) -> bool:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST + lid
        for l in self.lists:
            if l.PK == PK and l.SK == SK:
                return True
        return False
    
    def create(self, name: str):
        self.lists.append(List(name))

    def change_name(self, uid: str, lid: str, new_name: str):
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST + lid
        for l in self.lists:
            if l.PK == PK and l.SK == SK:
                l.name = new_name
                return
        raise Exception("List not found")

    def delete(self, uid: str, lid: str):
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST + lid
        for l in self.lists:
            if l.PK == PK and l.SK == SK:
                self.lists.remove(l)
                return
        raise Exception("List not found")

