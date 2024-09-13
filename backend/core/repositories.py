from abc import abstractmethod
from enum import Enum
from typing import List, Dict
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import GetCurrentTimeInSeconds
from .globals import DB_PREFIX_USER, DB_PREFIX_SHOPPING_LIST, DB_PREFIX_RECIPE, DB_PREFIX_ITEM
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


class Recipe(GenenericRepo):
    def __init__(self, userid: str, name: str, instructions: List[str], servings: int):
        super().__init__(DB_PREFIX_USER + userid, DB_PREFIX_RECIPE + generate())

        self.name = name
        self.instructions = instructions
        self.servings = servings

class RecipeRepo(GenenericRepo):
    recipes: List[Recipe] = []

    def get(self, uid: str, rid: str) -> Recipe:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_RECIPE + rid
        for r in self.recipes:
            if r.PK == PK and r.SK == SK:
                return r
        raise Exception("Recipe not found")
    
    def recipe_exists(self, uid: str, rid: str) -> bool:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_RECIPE + rid
        for r in self.recipes:
            if r.PK == PK and r.SK == SK:
                return True
        return False
    
    def create(self, name: str, instructions: List[str], servings: int):
        self.recipes.append(Recipe(name, instructions, servings))

    def delete(self, uid: str, rid: str):
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_RECIPE + rid
        for r in self.recipes:
            if r.PK == PK and r.SK == SK:
                self.recipes.remove(r)
                return
        raise Exception("Recipe not found")
    
    def get_all(self, uid: str):
        PK = DB_PREFIX_USER + uid
        return [r for r in self.recipes if r.PK == PK]
    
ItemType = Enum('ItemType', 'user list recipe')
class Item(GenericModel):
    def __init__(self, type: ItemType, userid: str, name: str, quantity: int, unit: str, price: float, expiresAt: int):
        prefix = DB_PREFIX_USER if type == ItemType.user else \
                 DB_PREFIX_SHOPPING_LIST if type == ItemType.list else \
                 DB_PREFIX_RECIPE
        super().__init__(prefix + userid, DB_PREFIX_ITEM + generate())
        
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.price = price
        self.expiresAt = expiresAt

class ItemRepo(GenenericRepo):
    userItems: Dict[str, List[Item]] = {}
    listItems: Dict[str, List[Item]] = {}
    recipeItems: Dict[str, List[Item]] = {}

    def get(self, ItemType: ItemType, pkid: str, skid: str) -> Item:
        if ItemType == ItemType.user:
            PK = DB_PREFIX_USER + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.userItems[PK]:
                if i.SK == SK:
                    return i
        elif ItemType == ItemType.list:
            PK = DB_PREFIX_SHOPPING_LIST + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.listItems[PK]:
                if i.SK == SK:
                    return i
        elif ItemType == ItemType.recipe:
            PK = DB_PREFIX_RECIPE + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.recipeItems[PK]:
                if i.SK == SK:
                    return i
        else:
            raise Exception("Invalid ItemType")
        raise Exception("Item not found")
    
    def item_exists(self, ItemType: ItemType, pkid: str, skid: str) -> bool:
        if ItemType == ItemType.user:
            PK = DB_PREFIX_USER + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.userItems[PK]:
                if i.SK == SK:
                    return True
        elif ItemType == ItemType.list:
            PK = DB_PREFIX_SHOPPING_LIST + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.listItems[PK]:
                if i.SK == SK:
                    return True
        elif ItemType == ItemType.recipe:
            PK = DB_PREFIX_RECIPE + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.recipeItems[PK]:
                if i.SK == SK:
                    return True
        else:
            raise Exception("Invalid ItemType")
        return False
    
    def get_all(self, ItemType: ItemType, pkid: str):
        if ItemType == ItemType.user:
            PK = DB_PREFIX_USER + pkid
            return self.userItems[PK]
        elif ItemType == ItemType.list:
            PK = DB_PREFIX_SHOPPING_LIST + pkid
            return self.listItems[PK]
        elif ItemType == ItemType.recipe:
            PK = DB_PREFIX_RECIPE + pkid
            return self.recipeItems[PK]
        else:
            raise Exception("Invalid ItemType")
        
    def create(self, type: ItemType, name: str, quantity: int, unit: str, price: float, expiresAt: int):
        if type not in ItemType:
            raise Exception("Invalid ItemType")
        item = Item(type, name, quantity, unit, price, expiresAt)
        if type == ItemType.user:
            self.userItems[item.PK].append(item)
        elif type == ItemType.list:
            self.listItems[item.PK].append(item)
        elif type == ItemType.recipe:
            self.recipeItems[item.PK].append(item)

    def delete(self, ItemType: ItemType, pkid: str, skid: str):
        if ItemType == ItemType.user:
            PK = DB_PREFIX_USER + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.userItems[PK]:
                if i.SK == SK:
                    self.userItems[PK].remove(i)
                    return
        elif ItemType == ItemType.list:
            PK = DB_PREFIX_SHOPPING_LIST + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.listItems[PK]:
                if i.SK == SK:
                    self.listItems[PK].remove(i)
                    return
        elif ItemType == ItemType.recipe:
            PK = DB_PREFIX_RECIPE + pkid
            SK = DB_PREFIX_ITEM + skid
            for i in self.recipeItems[PK]:
                if i.SK == SK:
                    self.recipeItems[PK].remove(i)
                    return
        else:
            raise Exception("Invalid ItemType")
        raise Exception("Item not found")


    