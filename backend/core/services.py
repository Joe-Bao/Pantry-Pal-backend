# services.py
from .repositories import ShoppingListRepo, UserRepo, RecipeRepo, ItemRepo, ItemType
from datetime import datetime
from typing import List

class UserService:
    def __init__(self):
        self.user_repo = UserRepo()

    def register_user(self, username: str, password: str, email: str, birthday: str):
        if not username or not password or not email or not birthday:
            raise ValueError("All fields are required")

        try:
            datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")
        
        if self.user_repo.username_exists(username):
            raise ValueError("User already exists")

        self.user_repo.create(username, password, email, birthday)

    def login_user(self, username: str, password: str):
        if not username or not password:
            raise ValueError("Username and password are required")

        if not self.user_repo.authenticate_user(username, password):
            raise ValueError("Incorrect username or password")

        # Here, you can add more logic like generating a token or managing sessions
        return True
        
    def get_user_settings(self, username: str):
        user = self.user_repo.get(username)
        return {
            'username': user.username,
            'email': user.email,
            'birthday': user.birthday,
            'allergies': user.allergies,
            'diets': user.diets,
            'intolerances': user.intolerances,
        }

    def update_user_settings(self, username: str, data: dict):
        user = self.user_repo.get(username)
        if 'email' in data:
            user.email = data['email']
        if 'birthday' in data:
            user.birthday = data['birthday']
        if 'allergies' in data:
            user.allergies = data['allergies']
        if 'diets' in data:
            user.diets = data['diets']
        if 'intolerances' in data:
            user.intolerances = data['intolerances']

        return user
    
class ShoppingListService:
    def __init__(self):
        self.list_repo = ShoppingListRepo()

    def create_list(self, userid: str, name: str): #create
        if not userid or not name:
            raise ValueError("All fields are required")

        self.list_repo.create(userid, name)
        
    def get_list_info(self, userid: str, listid: str):
        list = self.list_repo.get(userid, listid)
        return {
            'name': list.name
        }

    def change_listname(self, userid: str, listid: str, newname: str):
        self.list_repo.change_name(userid, listid, newname)

        return {
            'name': newname,
        }
        
    def delete_list(self, userid: str, listid: str):
        self.list_repo.delete(userid, listid)

class RecipeRepo:
    def __init__(self):
        self.recipe_repo = RecipeRepo()

    def create_recipe(self, userid: str, name: str, instructions: List[str], servings: int):
        if not userid or not name or not instructions or servings <= 0:
            raise ValueError("All fields are required and servings must be positive")

        if self.recipe_repo.recipe_exists(userid, name):
            raise ValueError("Recipe with this name already exists")

        self.recipe_repo.create(name, instructions, servings)
    
    def get_recipe_info(self, userid: str, recipeid: str):
        recipe = self.recipe_repo.get(userid, recipeid)
        return {
            'name': recipe.name,
            'instructions': recipe.instructions,
            'servings': recipe.servings
        }

    def change_recipe_name(self, userid: str, recipeid: str, newname: str):
        recipe = self.recipe_repo.get(userid, recipeid)
        if not recipe:
            raise Exception("Recipe not found")

        if self.recipe_repo.recipe_exists(userid, newname):
            raise ValueError("Recipe with this new name already exists")

        self.recipe_repo.delete(userid, recipeid)
        self.recipe_repo.create(newname, recipe.instructions, recipe.servings)

        return {
            'name': newname,
        }
        
    def delete_recipe(self, userid: str, recipeid: str):
        if not self.recipe_repo.recipe_exists(userid, recipeid):
            raise Exception("Recipe not found")

        self.recipe_repo.delete(userid, recipeid)
    
    def get_all_recipes(self, userid: str):
        return self.recipe_repo.get_all(userid)


class ItemService:
    def __init__(self):
        self.item_repo = ItemRepo()

    def create_item(self, type: ItemType, userid: str, name: str, quantity: int, unit: str, price: float, expiresAt: int):
        if not userid or not name or quantity < 0 or price < 0 or expiresAt < 0:
            raise ValueError("All fields are required and must be valid")

        self.item_repo.create(type, name, quantity, unit, price, expiresAt)
    
    def get_item_info(self, type: ItemType, userid: str, itemid: str):
        item = self.item_repo.get(type, userid, itemid)
        return {
            'name': item.name,
            'quantity': item.quantity,
            'unit': item.unit,
            'price': item.price,
            'expiresAt': item.expiresAt
        }

    def update_item(self, type: ItemType, userid: str, itemid: str, name: str = None, quantity: int = None, unit: str = None, price: float = None, expiresAt: int = None):
        item = self.item_repo.get(type, userid, itemid)
        
        if name is not None:
            item.name = name
        if quantity is not None:
            item.quantity = quantity
        if unit is not None:
            item.unit = unit
        if price is not None:
            item.price = price
        if expiresAt is not None:
            item.expiresAt = expiresAt
        
        # Assuming the repo reflects changes directly, otherwise you would need to update the repo here.

        return {
            'name': item.name,
            'quantity': item.quantity,
            'unit': item.unit,
            'price': item.price,
            'expiresAt': item.expiresAt
        }
    
    def delete_item(self, type: ItemType, userid: str, itemid: str):
        self.item_repo.delete(type, userid, itemid)