from abc import abstractmethod
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import GetCurrentTimeInSeconds, ItemTypePrefix
from .globals import DB_INDEX_USERNAME, DB_PREFIX_ITEM, DB_PREFIX_RECIPE, DB_PREFIX_USER, DB_PREFIX_SHOPPING_LIST, ItemType
from nanoid import generate
import boto3

resource = boto3.resource('dynamodb')
db_table = resource.Table('DjangoTest')

class GenericModel(object):
    def __init__(self, PK, SK, createdAt=None, modifiedAt=None):
        now = GetCurrentTimeInSeconds()
        self.PK = PK
        self.SK = SK
        self.createdAt = now if createdAt is None else createdAt
        self.modifiedAt = now if modifiedAt is None else modifiedAt

class GenenericRepo(object):
    @abstractmethod
    def get(self, PK: str, SK: str):
        pass

    @abstractmethod
    def delete(self, PK: str, SK: str):
        pass


class User(GenericModel):
    def __init__(
            self,
            PK: str,
            SK: str,
            username: str,
            password: str,
            email: str,
            birthday: str,
            allergies: List[str] = [],
            diets: List[str] = [],
            intolerances: List[str] = [],
            createdAt=None,
            modifiedAt=None
        ):
        super().__init__(PK, SK, createdAt, modifiedAt)
        
        self.username = username
        self.password = password # needs to be hashed before passing to this class
        self.email = email
        self.birthday = birthday
        self.allergies = allergies
        self.diets = diets
        self.intolerances = intolerances


class UserRepo(GenenericRepo):
    def get(self, id: str) -> User:
        PK = DB_PREFIX_USER + id
        resp = db_table.get_item(
            Key={"PK": PK, "SK": PK},
        )
        if "Item" not in resp:
            raise TypeError("User not found")
        return User(**resp["Item"])
        
    def get_by_username(self, username: str) -> User:
        resp = db_table.query(
            IndexName=DB_INDEX_USERNAME,
            KeyConditionExpression="#username = :username",
            ExpressionAttributeNames={"#username": "username"},
            ExpressionAttributeValues={":username": username}
        )
        if "Items" not in resp or len(resp["Items"]) == 0:
            raise TypeError("User not found")
        return User(**resp["Items"][0])
    
    def user_exists(self, id: str) -> bool:
        try:
            self.get(id)
            return True
        except TypeError:
            return False
    
    def username_exists(self, username: str) -> bool:
        try:
            self.get_by_username(username)
            return True
        except TypeError:
            return False
    
    def create(self, username: str, password: str, email: str, birthday: str) -> User:
        id = generate()
        PK = DB_PREFIX_USER + id
        SK = DB_PREFIX_USER + id
        hashed_password = generate_password_hash(password)

        user = User(PK, SK, username, hashed_password, email, birthday)
        db_table.put_item(Item=vars(user))

        return user

    def authenticate_user(self, username: str, password: str) -> User:
        try:
            user = self.get_by_username(username)
            if check_password_hash(user.password, password):
                return user
            return None
        except TypeError:
            return None
        
    def update(self, id: str, data: dict) -> User:
        PK = DB_PREFIX_USER + id

        now = GetCurrentTimeInSeconds()
        UpdateExpression="SET #modifiedAt = :modifiedAt"
        ExpressionAttributeNames={"#modifiedAt": "modifiedAt"}
        ExpressionAttributeValues={":modifiedAt": now}

        for key in data:
            UpdateExpression += f", #{key} = :{key}"
            ExpressionAttributeNames["#" + key] = key
            ExpressionAttributeValues[":" + key] = data[key]
        
        resp = db_table.update_item(
            Key={"PK": PK, "SK": PK},
            UpdateExpression=UpdateExpression,
            ExpressionAttributeNames=ExpressionAttributeNames,
            ExpressionAttributeValues=ExpressionAttributeValues,
            ReturnValues="ALL_NEW"
        )

        return User(**resp["Attributes"])


class ShoppingList(GenericModel):
    def __init__(
            self,
            PK: str,
            SK: str,
            name: str,
            createdAt=None,
            modifiedAt=None
        ):
        super().__init__(PK, SK, createdAt, modifiedAt)
        
        self.name = name

class ShoppingListRepo(GenenericRepo):
    def get(self, uid: str, lid: str) -> ShoppingList:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST + lid
        resp = db_table.get_item(
            Key={"PK": PK, "SK": SK},
        )
        if "Item" not in resp or len(resp["Item"]) == 0:
            raise TypeError("List not found")
        return ShoppingList(**resp["Item"])
    
    def get_all(self, uid: str) -> List[ShoppingList]:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST
        resp = db_table.query(
            KeyConditionExpression="#PK = :PK AND begins_with(#SK, :SK)",
            ExpressionAttributeNames={"#PK": "PK", "#SK": "SK"},
            ExpressionAttributeValues={":PK": PK, ":SK": SK}
        )
        return [ShoppingList(**item) for item in resp["Items"]]
    
    def list_exists(self, uid: str, lid: str) -> bool:
        try:
            self.get(uid, lid)
            return True
        except TypeError:
            return False
    
    def create(self, userId: str, name: str) -> ShoppingList:
        id = generate()
        PK = DB_PREFIX_USER + userId
        SK = DB_PREFIX_SHOPPING_LIST + id
        
        list = ShoppingList(PK, SK, name)
        db_table.put_item(Item=vars(list))

        return list

    def change_name(self, uid: str, lid: str, new_name: str) -> ShoppingList:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST + lid
        
        db_table.update_item(
            Key={"PK": PK, "SK": SK},
            UpdateExpression="SET #name = :name, #modifiedAt = :modifiedAt",
            ExpressionAttributeNames={"#name": "name", "#modifiedAt": "modifiedAt"},
            ExpressionAttributeValues={":name": new_name, ":modifiedAt": GetCurrentTimeInSeconds()},
        )

        return ShoppingList(PK, SK, new_name)

    def delete(self, uid: str, lid: str):
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST + lid
        
        db_table.delete_item(
            Key={"PK": PK, "SK": SK}
        )

    def delete_all(self, uid: str):
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_SHOPPING_LIST
        resp = db_table.query(
            KeyConditionExpression="#PK = :PK AND begins_with(#SK, :SK)",
            ExpressionAttributeNames={"#PK": "PK", "#SK": "SK"},
            ExpressionAttributeValues={":PK": PK, ":SK": SK}
        )
        with db_table.batch_writer() as batch:
            for item in resp["Items"]:
                batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})


class Recipe(GenenericRepo):
    def __init__(
            self,
            PK: str,
            SK: str,
            name: str,
            instructions: List[str],
            servings: int,
            diets: List[str],
            summary: str,
            img: str,
            readyInMinutes: int,
            createdAt=None,
            modifiedAt=None
        ):
        super().__init__(PK, SK, createdAt, modifiedAt)

        self.name = name
        self.instructions = instructions
        self.servings = servings
        self.diets = diets  # List of dietary restrictions (e.g., ['gluten free', 'dairy free'])
        self.summary = summary  # Brief summary of the recipe
        self.img = img  # URL of the recipe image
        self.readyInMinutes = readyInMinutes  # Time required to prepare the dish

class RecipeRepo(GenenericRepo):
    def get(self, uid: str, rid: str) -> Recipe:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_RECIPE + rid
        resp = db_table.get_item(
            Key={"PK": PK, "SK": SK},
        )
        if "Item" not in resp or len(resp["Item"]) == 0:
            raise TypeError("Recipe not found")
        return Recipe(**resp["Item"])
    
    def get_all(self, uid: str):
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_RECIPE
        resp = db_table.query(
            KeyConditionExpression="#PK = :PK AND begins_with(#SK, :SK)",
            ExpressionAttributeNames={"#PK": "PK", "#SK": "SK"},
            ExpressionAttributeValues={":PK": PK, ":SK": SK}
        )
        return [Recipe(**item) for item in resp["Items"]]
    
    def recipe_exists(self, uid: str, rid: str) -> bool:
        try:
            self.get(uid, rid)
            return True
        except TypeError:
            return False
    
    def create(self, userid: str, name: str, instructions: List[str], servings: int):
        id = generate()
        PK = DB_PREFIX_USER + userid
        SK = DB_PREFIX_RECIPE + id
        
        recipe = Recipe(PK, SK, name, instructions, servings)
        db_table.put_item(Item=vars(recipe))
        return recipe
    
    def update(self, uid: str, rid: str, data: dict) -> Recipe:
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_RECIPE + rid

        now = GetCurrentTimeInSeconds()
        UpdateExpression="SET #modifiedAt = :modifiedAt"
        ExpressionAttributeNames={"#modifiedAt": "modifiedAt"}
        ExpressionAttributeValues={":modifiedAt": now}

        for key in data:
            UpdateExpression += f", #{key} = :{key}"
            ExpressionAttributeNames["#" + key] = key
            ExpressionAttributeValues[":" + key] = data[key]
        
        resp = db_table.update_item(
            Key={"PK": PK, "SK": SK},
            UpdateExpression=UpdateExpression,
            ExpressionAttributeNames=ExpressionAttributeNames,
            ExpressionAttributeValues=ExpressionAttributeValues,
            ReturnValues="ALL_NEW"
        )

        return Recipe(**resp["Attributes"])

    def delete(self, uid: str, rid: str):
        PK = DB_PREFIX_USER + uid
        SK = DB_PREFIX_RECIPE + rid
        resp = db_table.delete_item(
            Key={"PK": PK, "SK": SK}
        )
    

class Item(GenericModel):
    def __init__(
            self,
            PK: str,
            SK: str,
            name: str,
            quantity: int,
            unit: str,
            price: float,
            expiresAt: int,
            createdAt=None,
            modifiedAt=None
        ):
        
        super().__init__(PK, SK, createdAt, modifiedAt)
        
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.price = price
        self.expiresAt = expiresAt

class ItemRepo(GenenericRepo):
    def get(self, ItemType: ItemType, pkid: str, skid: str) -> Item:
        PK = ItemTypePrefix(ItemType) + pkid
        SK = DB_PREFIX_ITEM + skid
        resp = db_table.get_item(
            Key={"PK": PK, "SK": SK},
        )
        if "Item" not in resp or len(resp["Item"]) == 0:
            raise TypeError("Item not found")
        return Item(**resp["Item"])
    
    def item_exists(self, ItemType: ItemType, pkid: str, skid: str) -> bool:
        try:
            self.get(ItemType, pkid, skid)
            return True
        except TypeError:
            return False
    
    def get_all(self, ItemType: ItemType, pkid: str):
        PK = ItemTypePrefix(ItemType) + pkid
        SK = DB_PREFIX_ITEM
        resp = db_table.query(
            KeyConditionExpression="#PK = :PK AND begins_with(#SK, :SK)",
            ExpressionAttributeNames={"#PK": "PK", "#SK": "SK"},
            ExpressionAttributeValues={":PK": PK, ":SK": SK}
        )
        return [Item(**item) for item in resp["Items"]]
        
    def create(self, type: ItemType, pkid: str, name: str, quantity: int, unit: str, price: float, expiresAt: int):
        id = generate()
        PK = ItemTypePrefix(type) + pkid
        SK = DB_PREFIX_ITEM + id

        item = Item(PK, SK, name, quantity, unit, price, expiresAt)
        db_table.put_item(Item=vars(item))
        return item

    def update(self, ItemType: ItemType, pkid: str, skid: str, data: dict) -> Item:
        PK = ItemTypePrefix(ItemType) + pkid
        SK = DB_PREFIX_ITEM + skid

        now = GetCurrentTimeInSeconds()
        UpdateExpression="SET #modifiedAt = :modifiedAt"
        ExpressionAttributeNames={"#modifiedAt": "modifiedAt"}
        ExpressionAttributeValues={":modifiedAt": now}

        for key in data:
            UpdateExpression += f", #{key} = :{key}"
            ExpressionAttributeNames["#" + key] = key
            ExpressionAttributeValues[":" + key] = data[key]
        
        resp = db_table.update_item(
            Key={"PK": PK, "SK": SK},
            UpdateExpression=UpdateExpression,
            ExpressionAttributeNames=ExpressionAttributeNames,
            ExpressionAttributeValues=ExpressionAttributeValues,
            ReturnValues="ALL_NEW"
        )

        return Item(**resp["Attributes"])

    def delete(self, ItemType: ItemType, pkid: str, skid: str):
        PK = ItemTypePrefix(ItemType) + pkid
        SK = DB_PREFIX_ITEM + skid
        resp = db_table.delete_item(
            Key={"PK": PK, "SK": SK}
        )

    def delete_all(self, ItemType: ItemType, pkid: str):
        PK = ItemTypePrefix(ItemType) + pkid
        SK = DB_PREFIX_ITEM
        resp = db_table.query(
            KeyConditionExpression="#PK = :PK AND begins_with(#SK, :SK)",
            ExpressionAttributeNames={"#PK": "PK", "#SK": "SK"},
            ExpressionAttributeValues={":PK": PK, ":SK": SK}
        )
        with db_table.batch_writer() as batch:
            for item in resp["Items"]:
                batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})


    