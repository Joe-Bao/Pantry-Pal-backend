from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import UserService
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            
            # Parse JSON body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # Validate fields and register user
            user_service = UserService()
            user_service.register_user(username, password, email)
            
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login(request):
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
