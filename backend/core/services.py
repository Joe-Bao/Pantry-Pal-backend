# services.py
import re
import boto3

from .settings import RAPIDAPI_KEY
from .globals import UNIT_ABBREVIATIONS_PLURAL, UNIT_ABBREVIATIONS_TO_WORD, UNIT_SINGULAR_TO_PLURAL
from .repositories import ShoppingList, ShoppingListRepo, User, UserRepo, RecipeRepo, Recipe, ItemRepo, Item, ItemType
from datetime import datetime
from typing import List
import requests
import asyncio

client = boto3.client('textract')

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
    
    def user_exists(self, id: str) -> bool:
        return self.user_repo.user_exists(id)

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
    
    def list_exists(self, userid: str, listid: str) -> bool:
        return self.list_repo.list_exists(userid, listid)

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

    def create_recipe(self, userid: str, name: str, instructions: List[str], servings: int, diets: List[str], summary: str, img: str, readyInMinutes: int) -> Recipe:
        if not userid or not name or not instructions or servings <= 0:
            raise ValueError("All fields are required and servings must be positive")

        if self.recipe_repo.recipe_exists(userid, name):
            raise ValueError("Recipe with this name already exists")
        return self.recipe_repo.create(userid, name, instructions, servings, diets, summary, img, readyInMinutes)
    
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
    
    def batch_create_items(self, type: ItemType, pkid: str, items: List[dict]) -> List[Item]:
        return self.item_repo.batch_create(type, pkid, items)

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

    def get_all_items(self, type: ItemType, pkId: str) -> List[Item]:
        return self.item_repo.get_all(type, pkId)

class OCRService:
    def __init__(self):
        self.client = client

    def extract_lines(self, image: bytes) -> List[str]:
        response = self.client.detect_document_text(Document={'Bytes': image})
        return [item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE']

    def shopping_list_parser(self, lines: List[str]) -> List[Item]:
        if "list" in lines[0].lower():
            lines = lines[1:]
        
        # remove non alphanumeric characters
        for i in range(len(lines)):
            lines[i] = re.sub(r'[^a-zA-Z0-9\s]', '', lines[i])
        
        # find quantity and unit
        items = []
        for line in lines:
            # print(line)
            words = line.lower().split(" ")
            quantity = None
            unit = None
            name = ""
            for word in words:
                if quantity is None:
                    numChars = re.sub(r'\D', '', word)
                    letterChars = re.sub(r'[^a-zA-Z]', '', word)
                    # print(numChars, letterChars)
                    # if word has no numbers, not a quantity
                    if len(numChars) == 0:
                        name += word + " "
                        continue
                    
                    quantity = int(numChars)
                        
                    # check for abbreviated units (e.g. 500g, 2tbsp)
                    if letterChars in UNIT_ABBREVIATIONS_TO_WORD:
                        unit = UNIT_ABBREVIATIONS_TO_WORD[letterChars]
                    continue
                if unit is None:
                    if word in UNIT_ABBREVIATIONS_PLURAL:
                        unit = word
                    elif word in UNIT_SINGULAR_TO_PLURAL:
                        unit = UNIT_SINGULAR_TO_PLURAL[word]
                    else:
                        name += word + " "
                    continue

                name += word + " "
            # make sure nothing is empty
            # print(name, quantity, unit)
            if len(name) == 0:
                continue # skip this line
            if quantity is None:
                quantity = 1
            if unit is None:
                unit = "unit"
            # print(name, quantity, unit)
            items.append(Item(PK="", SK="", name=name.strip(), quantity=quantity, unit=unit, price=0, expiresAt=0, ))

        return items

class WoolworthsService():
    def get_item_by_barcode(self, barcode: str): 
        url = "https://woolworths-products-api.p.rapidapi.com/woolworths/barcode-search/" + barcode

        headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "woolworths-products-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)

        # self.amt = ""
        # self.unit = ""
        # for x in response.json()['product_size']:
        #     if x.isdigit():
        #         self.amt = self.amt + x
        #     else:
        #         self.unit = self.unit + x

        # self.barcode = int(response.json()['barcode'])
        # self.product_name = str(response.json()['product_name'])
        # self.product_brand = str(response.json()['product_brand'])
        # self.current_price = float(response.json()['current_price'])
        # self.product_amt = float(self.amt)
        # self.product_unit = self.unit
        # self.url = response.json()['url']
        
        # self.item = {"name" : self.product_name, 
        #         "brand" : self.product_brand,
        #         "amt" : self.product_amt,
        #         "unit" : self.product_unit,
        #         "price" : self.current_price,
        #         "url" : self.url
        # }
        # print(self.item)
        return response.json()
    

    def get_item_by_name(self, name: str):
        self.url = "https://woolworths-products-api.p.rapidapi.com/woolworths/product-search/"

        self.querystring = {"query":name}

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "woolworths-products-api.p.rapidapi.com"
        }

        response = requests.get(self.url, headers=headers, params=self.querystring)

        return(response.json()['results'][0])
    
    
    def get_product_list_by_name(self, name: str):
        self.url = "https://woolworths-products-api.p.rapidapi.com/woolworths/product-search/"

        self.querystring = {"query":name}

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "woolworths-products-api.p.rapidapi.com"
        }

        response = requests.get(self.url, headers=headers, params=self.querystring)

        return(response.json()['results'])

    async def async_batch_get_item_by_name(self, names: List[str]):
        return await asyncio.gather(*[asyncio.to_thread(self.get_item_by_name, name) for name in names])
    
    def batch_get_item_by_name(self, names: List[str]):
        return asyncio.run(self.async_batch_get_item_by_name(names))

class ApiService:
    def search_by_barcode_woolworths(self, barcode: str):
        url = f"https://woolworths-products-api.p.rapidapi.com/woolworths/barcode-search/{barcode}/"

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "woolworths-products-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the list of recipe previews (name and image)
        else:
            response.raise_for_status()  # Raise an error for bad responses


    def generate_recipe_preview(self, item_names: list[str], item_number: int) -> list:
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
        ingredients = ','.join(item_names)
        querystring = {
            "ingredients": ingredients,
            "number": item_number,
            "ignorePantry": "true",
            "ranking": "1"
        }
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,  # Use environment variable or config for sensitive data
            "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.json()  # Return the list of recipe previews (name and image)
        else:
            response.raise_for_status()  # Raise an error for bad responses

    def get_recipe_info_webApi(self, recipeWebId: str) -> dict:
        """
        Get detailed information for a recipe given its ID.

        Parameters:
        - recipe_id (int): The ID of the recipe to retrieve information for.

        Returns:
        - dict: A dictionary containing the recipe details.
        """
        url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipeWebId}/information"

        # Use the API key from Django settings
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

        # Send a GET request to the Spoonacular API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            # If the request fails, raise an error with the response content
            response.raise_for_status()
