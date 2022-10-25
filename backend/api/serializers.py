from rest_framework import serializers
from recipes.models import Ingredients, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'hexcolor',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
