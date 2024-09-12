from django.contrib import admin
from django.urls import path
from .views import ShoppingListAPIView, UserAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', UserAPIView.as_view(), name='user_api'),
    path('list/', ShoppingListAPIView.as_view(), name='shopping_list'),
]
