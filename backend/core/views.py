from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework import viewsets
from .serializers import ItemCreateSerializer, ItemPatchSerializer, ItemSerializer, RecipeCreateSerializer, RecipePatchSerializer, RecipeSerializer, ShoppingListCreateSerializer, ShoppingListPatchSerializer, ShoppingListSerializer, UserInfoPatchSerializer, UserLoginSerializer, UserRegisterSerializer, UserSerializer
from .services import UserService, ShoppingListService
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response


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
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_user_recipes',
        responses=RecipeSerializer(many=True)
    )
    def get_all_user_recipes(self, request, userId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_user_recipe',
        responses=RecipeSerializer
    )
    def get_user_recipe(self, request, userId, recipeId):
        pass
    
    @csrf_exempt
    @extend_schema(
        operation_id='delete_user_recipe',
        responses=None
    )
    def delete_user_recipe(self, request, userId, recipeId):
        pass

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
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='create_list_item',
        request=ItemCreateSerializer,
        responses=ItemSerializer
    )
    def create_list_item(self, request, userId, listId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='create_recipe_item',
        request=ItemCreateSerializer,
        responses=ItemSerializer
    )
    def create_recipe_item(self, request, userId, recipeId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_user_items',
        responses=ItemSerializer(many=True)
    )
    def get_all_user_items(self, request, userId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_list_items',
        responses=ItemSerializer(many=True)
    )
    def get_all_list_items(self, request, userId, listId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_all_recipe_items',
        responses=ItemSerializer(many=True)
    )
    def get_all_recipe_items(self, request, userId, recipeId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_user_item',
        responses=ItemSerializer
    )
    def get_user_item(self, request, userId, itemId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_list_item',
        responses=ItemSerializer
    )
    def get_list_item(self, request, userId, listId, itemId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='get_recipe_item',
        responses=ItemSerializer
    )
    def get_recipe_item(self, request, userId, recipeId, itemId):
        pass
    
    @csrf_exempt
    @extend_schema(
        operation_id='patch_user_item',
        request=ItemPatchSerializer,
        responses=ItemSerializer
    )
    def patch_user_item(self, request, userId, itemId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='patch_list_item',
        request=ItemPatchSerializer,
        responses=ItemSerializer
    )
    def patch_list_item(self, request, userId, listId, itemId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='patch_recipe_item',
        request=ItemPatchSerializer,
        responses=ItemSerializer
    )
    def patch_recipe_item(self, request, userId, recipeId, itemId):
        pass
    
    @csrf_exempt
    @extend_schema(
        operation_id='delete_user_item',
        responses=None
    )
    def delete_user_item(self, request, userId, itemId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='delete_list_item',
        responses=None
    )
    def delete_list_item(self, request, userId, listId, itemId):
        pass

    @csrf_exempt
    @extend_schema(
        operation_id='delete_recipe_item',
        responses=None
    )
    def delete_recipe_item(self, request, userId, recipeId, itemId):
        pass

        
    
