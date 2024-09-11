from django import views
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .services import UserService, ShoppingListService
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response

@csrf_exempt
class UserAPIView(views.APIView):
    
    def register(self, request):
        if request.method == 'POST':
            try:
                
                # Parse JSON body
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                email = data.get('email')
                birthday = data.get('birthday')
                # Validate fields and register user
                user_service = UserService()
                user_service.register_user(username, password, email, birthday)
                
                return JsonResponse({'message': 'User registered successfully'}, status=201)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    def login(self, request):
        if request.method == 'POST':
            try:
                # Parse JSON body
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')


                user_service = UserService()
                if user_service.login_user(username, password):
                    return JsonResponse({'message': 'Login successful'})
                else:
                    return JsonResponse({'error': 'Invalid username or password'}, status=401)

            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)


    @csrf_protect  # CSRF protection enabled
    @login_required  # Requires user to be logged in
    @require_http_methods(["GET", "PUT"])  # Restricts to GET and PUT requests only
    def user_settings(self, request):
        username = request.user.username  # Get the logged-in user's username
        user_service = UserService()
        if request.method == 'GET':
            try:
                user_data = user_service.get_user_settings(username)
                return JsonResponse(user_data, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=404)

        elif request.method == 'PUT':
            try:
                data = json.loads(request.body)
                updated_user = user_service.update_user_settings(username, data)
                return JsonResponse({'message': 'User settings updated successfully'}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    
@csrf_exempt
class ShoppingListAPIView(views.APIView):
    
    def get(self, request):
        user = request.user
        list_service = ListService()
        if request.method == 'GET':
            try:
                output = list_service.get_lists(user)
                return JsonResponse(output, status=200)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
        
    def patch(self, request):
        
    def delete(self, request):
        
/lists # return all lists for user -> ShoppingListAPIView
/lists/<list id> # return list with <list id> for user
/lists/<list id>/items # returns all items for specific list
/items/<item id>        
        
    