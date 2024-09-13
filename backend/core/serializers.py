from rest_framework import serializers
from .models import ShoppingList, LANGUAGE_CHOICES, STYLE_CHOICES


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ['id', 'title']
