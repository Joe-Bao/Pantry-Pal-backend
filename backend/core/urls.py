from django.contrib import admin
from django.urls import path
from .views import register, login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
