from django.contrib import admin
from django.urls import path
from .views import ItemViewSet, RecipeViewSet, ShoppingListViewSet, UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    # user urls
    path(
        'users/register/',
        UserViewSet.as_view({ 'post': 'register' }),
    ),
    path(
        'users/login/',
        UserViewSet.as_view({ 'post': 'login' }),
    ),
    path(
        'users/<str:userId>/',
        UserViewSet.as_view({ 'get': 'get_user', 'patch': 'patch_user' }),
    ),
    # shopping list urls
    path(
        'users/<str:userId>/lists/',
        ShoppingListViewSet.as_view({ 'get': 'get_all_user_lists', 'put': 'create_user_list', 'delete': 'delete_all_user_lists' }),
    ),
    path(
        'users/<str:userId>/lists/<str:listId>/',
        ShoppingListViewSet.as_view({ 'get': 'get_user_list', 'patch': 'patch_user_list', 'delete': 'delete_user_list' })
    ),
    # recipe urls
    path(
        'users/<str:userId>/recipes/',
        RecipeViewSet.as_view({'get': 'get_all_user_recipes', 'put': 'create_user_recipe'})
    ),
    
    # Get, update (PATCH), or delete a specific user recipe
    path(
        'users/<str:userId>/recipes/<str:recipeId>/',
        RecipeViewSet.as_view({
            'get': 'get_user_recipe',
            'patch': 'patch_recipe',
            'delete': 'delete_user_recipe'
        })
    ),
    # item urls
    path(
        'users/<str:userId>/lists/<str:listId>/items/',
        ItemViewSet.as_view({ 'get':'get_all_list_items', 'put': 'create_list_item' })
    ),
    path(
        'users/<str:userId>/recipes/<str:recipeId>/items/',
        ItemViewSet.as_view({ 'get':'get_all_recipe_items', 'put': 'create_recipe_item' })
    ),
    path(
        'users/<str:userId>/items/',
        ItemViewSet.as_view({ 'get':'get_all_user_items', 'put': 'create_user_item' })
    ),
    path(
        'users/<str:userId>/lists/<str:listId>/items/<str:itemId>/',
        ItemViewSet.as_view({ 'get': 'get_list_item', 'patch': 'patch_list_item', 'delete': 'delete_list_item' })
    ),
    path(
        'users/<str:userId>/recipes/<str:recipeId>/items/<str:itemId>/',
        ItemViewSet.as_view({ 'get': 'get_recipe_item', 'patch': 'patch_recipe_item', 'delete': 'delete_recipe_item' })
    ),
    path(
        'users/<str:userId>/items/<str:itemId>/',
        ItemViewSet.as_view({ 'get': 'get_user_item', 'patch': 'patch_user_item', 'delete': 'delete_user_item' })
    ),    
]
