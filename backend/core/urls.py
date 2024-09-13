from django.contrib import admin
from django.urls import path
from .views import ShoppingListAPIView, UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', UserViewSet.as_view(), basename = 'user'),
    path('lists/', ShoppingListAPIView.as_view(), name='shopping_list'),
    
]
