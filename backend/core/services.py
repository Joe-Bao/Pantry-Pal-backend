# services.py
from .repositories import ShoppingList, ShoppingListRepo, User, UserRepo, RecipeRepo, Recipe, ItemRepo, Item, ItemType
from datetime import datetime
from typing import List

class UserService:
    def __init__(self):
        self.user_repo = UserRepo()

    def register_user(self, username: str, password: str, email: str, birthday: str) -> User:
        if not username or not password or not email or not birthday:
            raise ValueError("All fields are required")

        try:
            datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")
        
        if self.user_repo.username_exists(username):
            raise ValueError("User already exists")

        return self.user_repo.create(username, password, email, birthday)

    def login_user(self, username: str, password: str) -> User:
        if not username or not password:
            raise ValueError("Username and password are required")

        user = self.user_repo.authenticate_user(username, password)
        if user is None:
            raise ValueError("Incorrect username or password")

        # Here, you can add more logic like generating a token or managing sessions
        return user
        
    def get_user(self, id: str) -> User:
        return self.user_repo.get(id)

    def update_user_settings(self, id: str, data: dict) -> User:
        if 'username' in data:
            raise ValueError("Username cannot be changed")
        
        return self.user_repo.update(id, data)
    
class ShoppingListService:
    def __init__(self):
        self.list_repo = ShoppingListRepo()

    def create_list(self, userid: str, name: str) -> ShoppingList: #create
        if not userid or not name:
            raise ValueError("All fields are required")

        return self.list_repo.create(userid, name)
        
    def get_list_info(self, userid: str, listid: str) -> ShoppingList:
        return self.list_repo.get(userid, listid)

    def change_listname(self, userid: str, listid: str, name: str) -> ShoppingList:
        return self.list_repo.change_name(userid, listid, name)
        
    def delete_list(self, userid: str, listid: str):
        self.list_repo.delete(userid, listid)

    def delete_all_lists(self, userid: str):
        self.list_repo.delete_all(userid)

    def get_all_lists(self, userid: str) -> List[ShoppingList]:
        return self.list_repo.get_all(userid)

# Services below may still need editing to work with views

class RecipeService:
    def __init__(self):
        self.recipe_repo = RecipeRepo()

    def create_recipe(self, userid: str, name: str, instructions: List[str], servings: int) -> Recipe:
        if not userid or not name or not instructions or servings <= 0:
            raise ValueError("All fields are required and servings must be positive")

        if self.recipe_repo.recipe_exists(userid, name):
            raise ValueError("Recipe with this name already exists")

        return self.recipe_repo.create(name, instructions, servings)
    
    def get_recipe_info(self, userid: str, recipeid: str) -> Recipe:
        return self.recipe_repo.get(userid, recipeid)

    def update_recipe(self, userid: str, recipe_id: str, data: dict) -> Recipe:
        return self.recipe_repo.update(userid, recipe_id, data)
        
    def delete_recipe(self, userid: str, recipeid: str):
        if not self.recipe_repo.recipe_exists(userid, recipeid):
            raise Exception("Recipe not found")

        self.recipe_repo.delete(userid, recipeid)
    
    def get_all_recipes(self, userid: str) -> List[Recipe]:
        return self.recipe_repo.get_all(userid)


class ItemService:
    def __init__(self):
        self.item_repo = ItemRepo()

    def create_item(self, type: ItemType, pkid: str, name: str, quantity: int, unit: str, price: float, expiresAt: int) -> Item:
        if not pkid or not name or quantity < 0 or price < 0 or expiresAt < 0:
            raise ValueError("All fields are required and must be valid")

        return self.item_repo.create(type, pkid, name, quantity, unit, price, expiresAt)
    
    def get_item_info(self, type: ItemType, pkid: str, itemid: str) -> Item:
        return self.item_repo.get(type, pkid, itemid)


    def update_item(self,type: ItemType, pkId: str, itemId: str, data: dict) -> Item:
        # Validate that the item exists
        if not self.item_repo.item_exists(type, pkId, itemId):
            raise ValueError("Item not found")

        # Update the item using the repository method
        return self.item_repo.update(ItemType, pkId, itemId, data)
    
    def delete_item(self, type: ItemType, pkId: str, itemid: str):
        self.item_repo.delete(type, pkId, itemid)

    def get_all_items(self, ItemType, pkId: str) -> List[Item]:
        return self.item_repo.get_all(ItemType, pkId)
