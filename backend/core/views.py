from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets
from .serializers import ItemCreateSerializer, ItemPatchSerializer, ItemSerializer, RecipeCreateSerializer, RecipePatchSerializer, RecipeSerializer, ShoppingListCreateSerializer, ShoppingListPatchSerializer, ShoppingListSerializer, UserInfoPatchSerializer, UserLoginSerializer, UserRegisterSerializer, UserSerializer, RecipePreviewSerializer
from .services import UserService, ShoppingListService, RecipeService, ItemService, ApiService
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response
from .repositories import ItemType

class UserViewSet(viewsets.ViewSet):
    @csrf_exempt
    @extend_schema(
        operation_id='register_user',
        request=UserRegisterSerializer,
        responses=UserSerializer
    )
    def register(self, request):
        if request.method == 'POST':
            try:
                # Parse JSON body
                data = json.loads(request.body)

                #Validate fields
                req_serializer = UserRegisterSerializer(data=data)
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Register user
                user_service = UserService()
                new_user = user_service.register_user(**req_serializer.validated_data)

                # Validate response
                res_serializer = UserSerializer(data=vars(new_user))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)

                # Return response
                return JsonResponse(res_serializer.data, status=201)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='login_user',
        request=UserLoginSerializer,
        responses=UserSerializer
    )
    def login(self, request):
        if request.method == 'POST':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                
                # Validate fields
                req_serializer = UserLoginSerializer(data=data)
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Login user
                user_service = UserService()
                user = user_service.login_user(**req_serializer.validated_data)

                # Validate response
                res_serializer = UserSerializer(data=vars(user))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)


    @csrf_exempt
    @extend_schema(
        operation_id='get_user',
        responses=UserSerializer
    )
    def get_user(self, request, userId):
        if request.method == 'GET':
            try:
                user_service = UserService()
                user = user_service.get_user(userId)
                res_serializer = UserSerializer(data=vars(user))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                return JsonResponse(res_serializer.data, status=200)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='patch_user',
        request=UserInfoPatchSerializer(partial=True),
        responses=UserSerializer
    )
    def patch_user(self, request, userId):
        if request.method == 'PATCH':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                
                # Validate fields
                req_serializer = UserInfoPatchSerializer(data=data, partial=True)
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Update user
                user_service = UserService()
                user = user_service.update_user_settings(userId, dict(req_serializer.validated_data))

                # Validate response
                res_serializer = UserSerializer(data=vars(user))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    
class ShoppingListViewSet(viewsets.ViewSet):   
    @csrf_exempt
    @extend_schema(
        operation_id='create_user_list',
        request=ShoppingListCreateSerializer,
        responses=ShoppingListSerializer
    )
    def create_user_list(self, request, userId):
        if request.method == 'PUT':
            try:
                # Parse JSON body
                data = json.loads(request.body)

                # Validate fields
                req_serializer = ShoppingListCreateSerializer(data=data)
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Create list
                list_service = ShoppingListService()
                list = list_service.create_list(userId, **req_serializer.validated_data)

               # Validate response
                res_serializer = ShoppingListSerializer(data=vars(list))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='get_all_user_lists',
        responses=ShoppingListSerializer(many=True)
    )
    def get_all_user_lists(self, request, userId):
        if request.method == 'GET':
            try:
                list_service = ShoppingListService()
                lists = list_service.get_all_lists(userId)
                res_serializer = ShoppingListSerializer(data=[vars(l) for l in lists], many=True)
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_user_list',
        responses=ShoppingListSerializer
    )
    def get_user_list(self, request, userId, listId):
        if request.method == 'GET':
            try:
                list_service = ShoppingListService()
                list = list_service.get_list_info(userId, listId)
                res_serializer = ShoppingListSerializer(data=vars(list))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                return JsonResponse(res_serializer.data, status=200)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='patch_user_list',
        request=ShoppingListPatchSerializer,
        responses=ShoppingListSerializer
    )
    def patch_user_list(self, request, userId, listId):
        if request.method == 'PATCH':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                
                # Validate fields
                req_serializer = ShoppingListPatchSerializer(data=data, partial=True)
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Update list
                list_service = ShoppingListService()
                list = list_service.change_listname(userId, listId, **req_serializer.validated_data)

                # Validate response
                res_serializer = ShoppingListSerializer(data=vars(list))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='delete_all_user_lists',
        responses=None
    )
    def delete_all_user_lists(self, request, userId):
        if request.method == 'DELETE':
            try:
                list_service = ShoppingListService()
                list_service.delete_all_lists(userId)
                return JsonResponse({}, status=204)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='delete_user_list',
        responses=None
    )
    def delete_user_list(self, request, userId, listId):
        if request.method == 'DELETE':
            try:
                list_service = ShoppingListService()
                list_service.delete_list(userId, listId)
                return JsonResponse({}, status=204)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
# Implement the repos below in the same style as done above (copy and modify the code if needed)

class RecipeViewSet(viewsets.ViewSet):
    @csrf_exempt
    @extend_schema(
        operation_id='create_user_recipe',
        request=RecipeCreateSerializer,
        responses=RecipeSerializer
    )
    def create_user_recipe(self, request, userId):
        if request.method == 'PUT':
            try:
                # Parse JSON body
                data = json.loads(request.body)

                # Validate fields
                req_serializer = RecipeCreateSerializer(data=data)
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Create recipe
                recipe_service = RecipeService()
                recipe = recipe_service.create_list(userId, **req_serializer.validated_data)

               # Validate response
                res_serializer = RecipeSerializer(data=vars(recipe))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_user_recipes',
        responses=RecipeSerializer(many=True)
    )
    def get_all_user_recipes(self, request, userId):
        if request.method == 'GET':
            try:
                recipe_service = RecipeService()
                recipes = recipe_service.get_all_lists(userId)
                res_serializer = ShoppingListSerializer(data=[vars(r) for r in recipes], many=True)
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_user_recipe',
        responses=RecipeSerializer
    )
    def get_user_recipe(self, request, userId, recipeId):
        if request.method == 'GET':
            try:
                recipe_service = RecipeService()  # Use the RecipeService for fetching recipe info
                recipe = recipe_service.get_recipe_info(userId, recipeId)  # Fetch recipe based on userId and recipeId
                res_serializer = RecipeSerializer(data=vars(recipe))  # Use the appropriate RecipeSerializer
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                return JsonResponse(res_serializer.data, status=200)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='delete_user_recipe',
        responses=None
    )
    def patch_recipe(request, userId, recipeId):
        if request.method == 'PATCH':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                
                # Validate fields
                req_serializer = RecipePatchSerializer(data=data, partial=True)
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Update recipe
                recipe_service = RecipeService()
                recipe = recipe_service.update_recipe(userId, recipeId, dict(req_serializer.validated_data))

                # Validate response
                res_serializer = RecipeSerializer(data=vars(recipe))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='delete_user_recipe',
        responses=None
    )
    def delete_user_recipe(self, request, userId, recipeId):
        if request.method == 'DELETE':
            try:
                recipe_service = RecipeService()  # Use the RecipeService to manage recipes
                recipe_service.delete_recipe(userId, recipeId)  # Delete the specific recipe
                return JsonResponse({}, status=204)  # Return a 204 No Content status
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='get_recipe_info_webApi',
        responses=object
    )
    def get_recipe_info_webApi(self, request, recipeWebId, userId, itemId):
        if request.method == 'GET':
            try:
                api_service = ApiService
                recipe_data = api_service.get_recipe_info_webApi(recipeWebId)
                recipe_info = {
                    'name': recipe_data['title'],  # Recipe name comes from the `title` field in JSON
                    'instructions': [recipe_data['instructions']] if isinstance(recipe_data['instructions'], str) else recipe_data['instructions'] or ["None"],
                    'servings': recipe_data['servings'],
                    'diets': recipe_data['diets'],
                    'summary': recipe_data['summary'] or 'None',
                    'img': recipe_data['image'],
                    'readyInMinutes': recipe_data['readyInMinutes']
                }
                recipe_serializer = RecipeCreateSerializer(data = recipe_info)
                ingredients = [
                    {
                        'name': ingredient['name'],
                        'quantity': ingredient['amount'],
                        'unit': ingredient['unit'],
                        'price': 0,
                        'expiresAt': 0,
                    }
                    for ingredient in recipe_data['extendedIngredients']
                ]
                ingredient_serializer = ItemCreateSerializer(data = ingredients, many = True)
                if not recipe_serializer.is_valid():
                    return JsonResponse(recipe_serializer.errors, status=500)
                if not ingredient_serializer.is_valid():
                    return JsonResponse(ingredient_serializer.errors, status=500)
                res_serializer = {
                    ItemType.list: recipe_serializer.data,        # Serialized recipe details
                    'ingredients': ingredient_serializer.data  # Serialized ingredients
                }
                return JsonResponse(res_serializer, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# Need to dynamically determine the item type based on the url used
# Example: /users/<userId>/items/ are pantry items
# Example: /users/<userId>/recipe/<recipeId>/items/ are recipe ingredients
# Example: /users/<userId>/lists/<listId>/items/ are shopping list items

class ItemViewSet(viewsets.ViewSet):
    @csrf_exempt
    @extend_schema(
        operation_id='create_user_item',
        request=ItemCreateSerializer,
        responses=ItemSerializer
    )
    def create_user_item(self, request, userId):
        if request.method == 'PUT':
            try:
                # Parse JSON body
                data = json.loads(request.body)

                # Validate fields using the appropriate serializer for items
                req_serializer = ItemCreateSerializer(data = data)  # Use ItemCreateSerializer for validation
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Create item using the ItemService
                item_service = ItemService()  # Use ItemService to create an item
                item = item_service.create_item(ItemType.user, userId, **req_serializer.validated_data)
                
                # Validate response using ItemSerializer
                res_serializer = ItemSerializer(data=vars(item))  # Use ItemSerializer for the response
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='create_list_item',
        request=ItemCreateSerializer,
        responses=ItemSerializer
    )
    def create_list_item(self, request, userId , listId):
        if request.method == 'PUT':
            try:
                # Parse JSON body
                data = json.loads(request.body)

                # Validate fields using the appropriate serializer for items
                req_serializer = ItemCreateSerializer(data = data)  # Use ItemCreateSerializer for validation
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Create item using the ItemService
                item_service = ItemService()  # Use ItemService to create an item
                item = item_service.create_item(ItemType.list, listId, **req_serializer.validated_data)

                # Validate response using ItemSerializer
                res_serializer = ItemSerializer(data=vars(item))  # Use ItemSerializer for the response
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='create_recipe_item',
        request=ItemCreateSerializer,
        responses=ItemSerializer
    )
    def create_recipe_item(self, request, userId, recipeId):
        if request.method == 'PUT':
            try:
                # Parse JSON body
                data = json.loads(request.body)

                # Validate fields using the appropriate serializer for items
                req_serializer = ItemCreateSerializer(data = data)  # Use ItemCreateSerializer for validation
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Create item using the ItemService
                item_service = ItemService()  # Use ItemService to create an item
                item = item_service.create_item(ItemType.list, recipeId, **req_serializer.validated_data)

                # Validate response using ItemSerializer
                res_serializer = ItemSerializer(data=vars(item))  # Use ItemSerializer for the response
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_user_items',
        responses=ItemSerializer(many=True)
    )
    def get_all_user_items(self, request, userId):
        if request.method == 'GET':
            try:
                # Use ItemService to fetch all items for the user
                item_service = ItemService()  # Assuming ItemService handles item-related operations
                items = item_service.get_all_items(ItemType.user, userId)  # Fetch all items for the user
                
                # Serialize the items using ItemSerializer
                res_serializer = ItemSerializer(data=[vars(i) for i in items], many=True)  # Serialize the items list
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return serialized data as JSON response
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='search_item_by_barcode',
        responses=ItemSerializer(many=True)
    )
    def search_item_by_barcode(self, request, userId, barCode):
        if request.method == 'GET':
            try:
                # Use ItemService to fetch all items for the user
                api_service = ApiService()  # Assuming ItemService handles item-related operations
                item_data = api_service.search_by_barcode_woolworths(barCode)  # Fetch all items for the user
                item_info = {
                    'name': item_data['product_name'],
                    'quantity': 1,
                    'unit': item_data['product_size'],
                    'price': float(item_data['current_price']),
                    'expiresAt': 0
                }
                # Serialize the items using ItemSerializer
                res_serializer = ItemCreateSerializer(data=item_info)  # Serialize the items list
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return serialized data as JSON response
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_list_items',
        responses=ItemSerializer
    )
    def get_all_list_items(self, request, userId, listId):
        if request.method == 'GET':
            try:
                # Use ItemService to fetch all items for the user
                item_service = ItemService()  # Assuming ItemService handles item-related operations
                items = item_service.get_all_items(ItemType.list, listId)  # Fetch all items for the user
                
                # Serialize the items using ItemSerializer
                res_serializer = ItemSerializer(data=[vars(i) for i in items], many=True)  # Serialize the items list
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return serialized data as JSON response
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_recipe_items',
        responses=ItemSerializer(many=True)
    )
    def get_all_recipe_items(self, request, userId, recipeId):
        if request.method == 'GET':
            try:
                # Use ItemService to fetch all items for the user
                item_service = ItemService()  # Assuming ItemService handles item-related operations
                items = item_service.get_all_items(ItemType.list, recipeId)  # Fetch all items for the user
                
                # Serialize the items using ItemSerializer
                res_serializer = ItemSerializer(data=[vars(i) for i in items], many=True)  # Serialize the items list
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return serialized data as JSON response
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_user_item',
        responses=ItemSerializer
    )
    def get_user_item(self, request, userId, itemId):
        if request.method == 'GET':
            try:
                # Use ItemService to fetch the item information based on userId and itemId
                item_service = ItemService()  # Assuming ItemService handles item-related operations
                item = item_service.get_item_info(ItemType.user, userId, itemId)  # Fetch item info using userId and itemId
                
                # Use the appropriate ItemSerializer to serialize the item data
                res_serializer = ItemSerializer(data=vars(item))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return the serialized item data in the response
                return JsonResponse(res_serializer.data, status=200)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='preview_user_item_recipes',
        responses=RecipePreviewSerializer(many=True)
    )
    def preview_user_item_recipes(self, request, userId, itemIds, number):
        if request.method == 'GET':
            try:
                item_id_list = itemIds.split(',')
                item_names = []
                item_service = ItemService()
                for itemId in item_id_list:
                    try:
                        # Use ItemService to fetch item information
                        item_service = ItemService()
                        item = item_service.get_item_info(ItemType.user, userId, itemId)
                        item_serializer = ItemSerializer(data=vars(item))
                        if not item_serializer.is_valid():
                            return JsonResponse(item_serializer.errors, status=500)
                        item_names.append(item_serializer.data['name'])
                    except Exception as e:  
                        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                api_service = ApiService()
                Response_recipes = api_service.generate_recipe_preview(item_names, number)
                recipe_previews = [
                    {
                        'id': recipe['id'],
                        'name': recipe['title'],
                        'img': recipe['image']
                    }
                    for recipe in Response_recipes
                ]
                res_serializer = RecipePreviewSerializer(data=recipe_previews, many=True)
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='get_list_item',
        responses=ItemSerializer
    )
    def get_list_item(self, request, userId, listId, itemId):
        if request.method == 'GET':
            try:
                # Use ItemService to fetch the item information based on userId and itemId
                item_service = ItemService()  # Assuming ItemService handles item-related operations
                item = item_service.get_item_info(ItemType.list, listId, itemId)  # Fetch item info using userId and itemId
                
                # Use the appropriate ItemSerializer to serialize the item data
                res_serializer = ItemSerializer(data=vars(item))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return the serialized item data in the response
                return JsonResponse(res_serializer.data, status=200)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)


    @csrf_exempt
    @extend_schema(
        operation_id='get_recipe_item',
        responses=ItemSerializer
    )
    def get_recipe_item(self, request, userId, recipeId, itemId):
        if request.method == 'GET':
            try:
                # Use ItemService to fetch the item information based on userId and itemId
                item_service = ItemService()  # Assuming ItemService handles item-related operations
                item = item_service.get_item_info(ItemType.list, recipeId, itemId)  # Fetch item info using userId and itemId
                
                # Use the appropriate ItemSerializer to serialize the item data
                res_serializer = ItemSerializer(data=vars(item))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return the serialized item data in the response
                return JsonResponse(res_serializer.data, status=200)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    
    @csrf_exempt
    @extend_schema(
        operation_id='patch_user_item',
        request=ItemPatchSerializer,
        responses=ItemSerializer
    )
    def patch_user_item(self, request, userId, itemId):
        if request.method == 'PATCH':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                
                # Validate fields
                req_serializer = ItemPatchSerializer(data=data, partial=True)  # Use the appropriate serializer for item updates
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Update item
                item_service = ItemService()
                item = item_service.update_item(ItemType.user, userId, itemId, **req_serializer.validated_data)

                # Validate response
                res_serializer = ItemSerializer(data=vars(item))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='patch_list_item',
        request=ItemPatchSerializer,
        responses=ItemSerializer
    )
    def patch_list_item(self, request, userId, listId, itemId):
        if request.method == 'PATCH':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                
                # Validate fields
                req_serializer = ItemPatchSerializer(data=data, partial=True)  # Use the appropriate serializer for item updates
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Update item
                item_service = ItemService()
                item = item_service.update_item(ItemType.list, listId, itemId, **req_serializer.validated_data)

                # Validate response
                res_serializer = ItemSerializer(data=vars(item))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='patch_recipe_item',
        request=ItemPatchSerializer,
        responses=ItemSerializer
    )
    def patch_recipe_item(self, request, userId, recipeId, itemId):
        if request.method == 'PATCH':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                
                # Validate fields
                req_serializer = ItemPatchSerializer(data=data, partial=True)  # Use the appropriate serializer for item updates
                if not req_serializer.is_valid():
                    return JsonResponse(req_serializer.errors, status=400)
                
                # Update item
                item_service = ItemService()
                item = item_service.update_item(ItemType.list, recipeId, itemId, **req_serializer.validated_data)

                # Validate response
                res_serializer = ItemSerializer(data=vars(item))
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                
                # Return response
                return JsonResponse(res_serializer.data, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    @csrf_exempt
    @extend_schema(
        operation_id='delete_user_item',
        responses=None
    )
    def delete_user_item(self, request, userId, itemId):
        if request.method == 'DELETE':
            try:
                item_service = ItemService()  # Use the ItemService to manage items
                item_service.delete_item(ItemType.user, userId, itemId)  # Delete the specific item
                return JsonResponse({}, status=204)  # Return a 204 No Content status
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='delete_list_item',
        responses=None
    )
    def delete_list_item(self, request, userId, listId, itemId):
        if request.method == 'DELETE':
            try:
                item_service = ItemService()  # Use the ItemService to manage items
                item_service.delete_item(ItemType.list, listId, itemId)  # Delete the specific item
                return JsonResponse({}, status=204)  # Return a 204 No Content status
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    @extend_schema(
        operation_id='delete_recipe_item',
        responses=None
    )
    def delete_recipe_item(self, request, userId, recipeId, itemId):
        if request.method == 'DELETE':
            try:
                item_service = ItemService()  # Use the ItemService to manage items
                item_service.delete_item(ItemType.list, recipeId, itemId)  # Delete the specific item
                return JsonResponse({}, status=204)  # Return a 204 No Content status
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)

        
    
