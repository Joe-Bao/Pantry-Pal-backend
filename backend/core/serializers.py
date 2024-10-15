from rest_framework import serializers
from .repositories import ShoppingList, User, Recipe, Item, ItemType


# USER SERIALIZERS

user_fields = {
    'PK': serializers.CharField(),
    'SK': serializers.CharField(),
    'username': serializers.CharField(max_length=100),
    'password': serializers.CharField(max_length=255, read_only=True),
    'email': serializers.EmailField(max_length=100),
    'birthday': serializers.CharField(max_length=10), #YYYY-MM-DD, 10 characters
    'allergies': serializers.ListField(child=serializers.CharField()),
    'diets': serializers.ListField(child=serializers.CharField()),
    'intolerances': serializers.ListField(child=serializers.CharField()),
    'createdAt': serializers.IntegerField(),
    'modifiedAt': serializers.IntegerField()
}
class UserSerializer(serializers.Serializer):
    PK = user_fields['PK']
    SK = user_fields['SK']
    username = user_fields['username']
    password = user_fields['password']
    email = user_fields['email']
    birthday = user_fields['birthday']
    allergies = user_fields['allergies']
    diets = user_fields['diets']
    intolerances = user_fields['intolerances']
    createdAt = user_fields['createdAt']
    modifiedAt = user_fields['modifiedAt']

class UserRegisterSerializer(serializers.Serializer):
    username = user_fields['username']
    password = serializers.CharField(max_length=255)
    email = user_fields['email']
    birthday = user_fields['birthday']

class UserLoginSerializer(serializers.Serializer):
    username = user_fields['username']
    password = serializers.CharField(max_length=255)

class UserInfoPatchSerializer(serializers.Serializer):
    email = user_fields['email']
    allergies = user_fields['allergies']
    diets = user_fields['diets']
    intolerances = user_fields['intolerances']

# SHOPPING LIST SERIALIZERS

shopping_list_fields = {
    'PK': serializers.CharField(),
    'SK': serializers.CharField(),
    'name': serializers.CharField(max_length=100),
    'createdAt': serializers.IntegerField(),
    'modifiedAt': serializers.IntegerField()
}

class ShoppingListSerializer(serializers.Serializer):
    PK = shopping_list_fields['PK']
    SK = shopping_list_fields['SK']
    name = shopping_list_fields['name']
    createdAt = shopping_list_fields['createdAt']
    modifiedAt = shopping_list_fields['modifiedAt']

class ShoppingListCreateSerializer(serializers.Serializer):
    name = shopping_list_fields['name']

class ShoppingListPatchSerializer(serializers.Serializer):
    name = shopping_list_fields['name']

# RECIPE SERIALIZERS

recipe_fields = {
    'PK': serializers.CharField(),
    'SK': serializers.CharField(),
    'name': serializers.CharField(max_length=100),
    'instructions': serializers.ListField(child=serializers.CharField()),
    'servings': serializers.IntegerField(),
    'diets': serializers.ListField(child=serializers.CharField()),  # New field for dietary restrictions
    'summary': serializers.CharField(max_length=512),  # New field for a brief summary
    'img': serializers.URLField(),  # New field for the image URL
    'readyInMinutes': serializers.IntegerField(),  # New field for preparation time
    'createdAt': serializers.IntegerField(),
    'modifiedAt': serializers.IntegerField()
}
    
class RecipeSerializer(serializers.Serializer):
    PK = recipe_fields['PK']
    SK = recipe_fields['SK']
    name = recipe_fields['name']
    instructions = recipe_fields['instructions']
    servings = recipe_fields['servings']
    diets = recipe_fields['diets']  # New field for dietary restrictions
    summary = recipe_fields['summary']  # New field for a brief summary
    img = recipe_fields['img']  # New field for the image URL
    readyInMinutes = recipe_fields['readyInMinutes']  # New field for preparation time
    createdAt = recipe_fields['createdAt']
    modifiedAt = recipe_fields['modifiedAt']

class RecipeCreateSerializer(serializers.Serializer):
    name = recipe_fields['name']
    instructions = recipe_fields['instructions']
    servings = recipe_fields['servings']
    diets = recipe_fields['diets']  # New field for dietary restrictions
    summary = recipe_fields['summary']  # New field for a brief summary
    img = recipe_fields['img']  # New field for the image URL
    readyInMinutes = recipe_fields['readyInMinutes']  # New field for preparation time

class RecipePatchSerializer(serializers.Serializer):
    name = recipe_fields['name']
    instructions = recipe_fields['instructions']
    servings = recipe_fields['servings']
    diets = recipe_fields['diets']  # New field for dietary restrictions
    summary = recipe_fields['summary']  # New field for a brief summary
    img = recipe_fields['img']  # New field for the image URL
    readyInMinutes = recipe_fields['readyInMinutes']  # New field for preparation time

# ITEM SERIALIZERS

item_fields = {
    'PK': serializers.CharField(),
    'SK': serializers.CharField(),
    'name': serializers.CharField(max_length=100),
    'quantity': serializers.DecimalField(max_digits=10, decimal_places=2),#cannot be float
    'unit': serializers.CharField(max_length=100),
    'price': serializers.DecimalField(max_digits=10, decimal_places=2),
    'expiresAt': serializers.IntegerField(),
    'createdAt': serializers.IntegerField(),
    'modifiedAt': serializers.IntegerField()
}

class ItemSerializer(serializers.Serializer):
    PK = item_fields['PK']
    SK = item_fields['SK']
    name = item_fields['name']
    quantity = item_fields['quantity']
    unit = item_fields['unit']
    price = item_fields['price']
    expiresAt = item_fields['expiresAt']
    createdAt = item_fields['createdAt']
    modifiedAt = item_fields['modifiedAt']

class ItemCreateSerializer(serializers.Serializer):
    name = item_fields['name']
    quantity = item_fields['quantity']
    unit = item_fields['unit']
    price = item_fields['price']
    expiresAt = item_fields['expiresAt']

class ItemPatchSerializer(serializers.Serializer):
    name = item_fields['name']
    quantity = item_fields['quantity']
    unit = item_fields['unit']
    price = item_fields['price']
    expiresAt = item_fields['expiresAt']

recipe_preview_fields = {
    'id': serializers.CharField(),  # Assuming ID is a string, adjust as necessary
    'name': serializers.CharField(max_length=100),
    'img': serializers.URLField()  # Adjust this if the image field requires a specific format (e.g., URL)
}

class RecipePreviewSerializer(serializers.Serializer):
    id = recipe_preview_fields['id']
    name = recipe_preview_fields['name']
    img = recipe_preview_fields['img']

Woolworth_item_fields = {
    'name': serializers.CharField(max_length=255),         # Product name
    'brand': serializers.CharField(max_length=100), # Brand of the product
    'current_price': serializers.FloatField(),              # Current price of the product
    'url': serializers.URLField()                           # Product URL
}

# Serializer for the items
class WoolworthItemSerializer(serializers.Serializer):
    name = Woolworth_item_fields['name']
    product_brand = Woolworth_item_fields['brand']
    current_price = Woolworth_item_fields['current_price']
    url = Woolworth_item_fields['url']