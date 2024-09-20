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
    'createdAt': serializers.IntegerField(),
    'modifiedAt': serializers.IntegerField()
}
    
class RecipeSerializer(serializers.Serializer):
    PK = recipe_fields['PK']
    SK = recipe_fields['SK']
    name = recipe_fields['name']
    instructions = recipe_fields['instructions']
    servings = recipe_fields['servings']
    createdAt = recipe_fields['createdAt']
    modifiedAt = recipe_fields['modifiedAt']

class RecipeCreateSerializer(serializers.Serializer):
    name = recipe_fields['name']
    instructions = recipe_fields['instructions']
    servings = recipe_fields['servings']

class RecipePatchSerializer(serializers.Serializer):
    name = recipe_fields['name']
    instructions = recipe_fields['instructions']
    servings = recipe_fields['servings']

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