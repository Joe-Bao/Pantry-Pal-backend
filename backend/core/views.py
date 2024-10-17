from typing import List
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .utils import GetQuantityFromProductSize, GetUnitFromProductSize, GetCurrentTimeInSeconds, roughMatchDiets
from .globals import ALLOWED_OCR_CONTENT_TYPES, UNIT_ABBREVIATIONS_PLURAL, ItemType
from .serializers import ItemCreateSerializer, ItemPatchSerializer, ItemSerializer, RecipeCreateSerializer, RecipePatchSerializer, RecipePreviewInfoSerializer, RecipeSerializer, ShoppingListCreateSerializer, ShoppingListPatchSerializer, ShoppingListSerializer, UserInfoPatchSerializer, UserLoginSerializer, UserRegisterSerializer, UserSerializer, RecipePreviewSerializer
from .services import OCRService, UserService, ShoppingListService, RecipeService, ItemService, WoolworthsService, ApiService
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
        operation_id='patch_user_recipe',
        request=RecipePatchSerializer,
        responses=RecipeSerializer
    )
    def patch_user_recipe(request, userId, recipeId):
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
        responses=RecipePreviewInfoSerializer
    )
    def get_recipe_info_webApi(self, request, userId, recipeWebId):
        if request.method == 'GET':
            try:
                # get recipe info from rapidapi
                api_service = ApiService()
                recipe_data = api_service.get_recipe_info_webApi(recipeWebId)

                # validate the recipe response
                recipe_info = {
                    'name': recipe_data['title'],  # Recipe name comes from the `title` field in JSON
                    'instructions': [recipe_data['instructions']] if isinstance(recipe_data['instructions'], str) else recipe_data['instructions'] or ["None"],
                    'servings': recipe_data['servings'],
                    'diets': recipe_data['diets'],
                    'summary': recipe_data['summary'] if 'summary' in recipe_data and len(recipe_data['summary']) < 512 else 'None',
                    'img': recipe_data['image'],
                    'readyInMinutes': recipe_data['readyInMinutes']
                }
                recipe_serializer = RecipeCreateSerializer(data = recipe_info)
                if not recipe_serializer.is_valid():
                    return JsonResponse(recipe_serializer.errors, status=500)

                # validate ingredients
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
                if not ingredient_serializer.is_valid():
                    return JsonResponse(ingredient_serializer.errors, status=500)
                
                # return the response
                res_serializer = {
                    'recipe': recipe_serializer.data,
                    'ingredients': ingredient_serializer.data
                }
                return JsonResponse(res_serializer, status=200, safe=False)
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
    def preview_user_item_recipes(self, request, userId, diets=None):
        if request.method == 'GET':
            try:
                # get all user items
                diets = request.query_params.get('diets', '')
                if diets:
                        diets_list = diets.split(',')
                item_service = ItemService()
                items = item_service.get_all_items(ItemType.user, userId)

                # filter for items that expire the soonest
                items = sorted(items, key=lambda x: x.expiresAt)

                # filter items that have expired already
                items = [item for item in items if item.expiresAt > GetCurrentTimeInSeconds()]
                # get the names of the items
                item_names = [item.name for item in items]
                # get the recipe previews, based on the item names
                api_service = ApiService()
                if diets:
                    Response_recipes = api_service.generate_recipe_preview(item_names, 15) # always return 15 recipes
                else:
                    Response_recipes = api_service.generate_recipe_preview(item_names, 6) # always return 6 recipes
                recipe_previews = [
                    {
                        'id': recipe['id'],
                        'name': recipe['title'],
                        'img': recipe['image']
                    }
                    for recipe in Response_recipes
                ]
                # validate the response      
                if diets:  
                    fit_recipes = []
                    for recipe in recipe_previews:
                        recipe_id = recipe['id']
                        # Fetch detailed info using the external API service
                        recipe_info = api_service.get_recipe_info_webApi(recipe_id)
                        
                        # Extract the diets property from the API response (it is a string list)
                        recipe_diets = recipe_info.get('diets', [])
                        
                        # Check if all diets in diets_list match with the recipe's diets
                        if roughMatchDiets(diets_list, recipe_diets):
                            fit_recipes.append(recipe)
                        # Stop when we have 6 matching recipes
                        if len(fit_recipes) >= 6:
                            break
                    res_serializer = RecipePreviewSerializer(data=fit_recipes, many=True)
                else:
                    res_serializer = RecipePreviewSerializer(data=recipe_previews, many=True)
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500)
                # return the response
                return JsonResponse(res_serializer.data, status=200, safe=False)
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
                    'quantity': GetQuantityFromProductSize(item_data['product_size']),
                    'unit': GetUnitFromProductSize(item_data['product_size']),
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
    
    @csrf_exempt
    @extend_schema(
        operation_id='create_list_items_from_image',
        request={
            "image/jpeg": { "type": "string", "format": "binary" },
            "image/png": { "type": "string", "format": "binary" }
        },
        responses=ItemSerializer(many=True)
    )
    def create_list_items_from_image(self, request, userId, listId):
        if request.method == 'POST':
            try:
                # No need to parse body, request.body is a bytestring
                # Check content type
                if request.content_type not in ALLOWED_OCR_CONTENT_TYPES:
                    return JsonResponse({'error': 'Invalid content type'}, status=415)

                # check if user exists
                user_service = UserService()
                if not user_service.user_exists(userId):
                    return JsonResponse({'error': 'User does not exist'}, status=400)
                
                # check if list exists
                list_service = ShoppingListService()
                if not list_service.list_exists(userId, listId):
                    return JsonResponse({'error': 'List does not exist'}, status=400)

                # Parse image using OCR service
                ocr_service = OCRService()
                lines = ocr_service.extract_lines(request.body)

                # parse shopping list into Item objects
                items = ocr_service.shopping_list_parser(lines)
                
                # create name strings to query Woolworths API (need consistent naming)
                item_search = []
                for i in items:
                    if i.quantity > 1:
                        if i.unit == 'unit':
                            item_search.append(f"{i.quantity} {i.name}")
                        else:
                            item_search.append(f"{i.name} {i.quantity}{UNIT_ABBREVIATIONS_PLURAL[i.unit]}")
                    else:
                        item_search.append(f"{i.name}")

                # query Woolworths API
                woolies = WoolworthsService()
                woolies_items = woolies.batch_get_item_by_name([f"{i.name}" for i in items])
                
                # create dicts compatible with ItemSerializer
                final_items: List[dict] = []
                for i in woolies_items:
                    final_items.append({
                        'name': i['product_name'],
                        'price': i['current_price'],
                        'quantity': GetQuantityFromProductSize(i['product_size']),
                        'unit': GetUnitFromProductSize(i['product_size']),
                        'expiresAt': 0
                    })

                # validate item dicts
                item_serializer = ItemCreateSerializer(data=final_items, many=True)
                if not item_serializer.is_valid():
                    return JsonResponse(item_serializer.errors, status=500)

                # add items to list in DB
                item_service = ItemService()
                db_items = item_service.batch_create_items(ItemType.list, listId, item_serializer.validated_data)

                # Validate response
                res_serializer = ItemSerializer(data=[vars(i) for i in db_items], many=True)
                if not res_serializer.is_valid():
                    return JsonResponse(res_serializer.errors, status=500, safe=False)
                
                return JsonResponse(res_serializer.data, status=200, safe=False)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

class PlaygroundViewSet(viewsets.ViewSet):
    def playground(self, request):
        woolies = WoolworthsService()
        print(woolies.batch_get_item_by_name(['penne pasta', 'gourmet tomatoes', 'jasmine rice 1kg', 'garam masala']))
        return JsonResponse({'message': 'Hello, world!'}, status=200)