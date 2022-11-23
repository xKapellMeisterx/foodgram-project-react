from django.core.validators import MinValueValidator
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (Favorite, Ingredient, IngredientMount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.serializers import CustomUserSerializer, CheckRequestMixin


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Tag."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientMountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделью IngredientMount при GET
    запросах к моделе Recipe.
    """

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientMount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделью IngredientMount при POST, PATCH, DEL
    запросах к моделе Recipe.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(validators=[MinValueValidator(1), ])

    class Meta:
        model = IngredientMount
        fields = (
            'id',
            'amount'
        )


class RecipeGetSerializer(serializers.ModelSerializer, CheckRequestMixin):
    """Сериализатор для работы с моделью Recipe при GET запросах."""

    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
            )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        self.good_request(request)
        return request.user.chooser.filter(recipe=obj).exists()

    def get_ingredients(self, obj):
        ingredients = IngredientMount.objects.filter(recipe=obj)
        return IngredientMountSerializer(ingredients, many=True).data

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        self.good_request(request)
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class RecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделью Recipe при POST, PATCH, DEL запросах.
    """

    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'author',
            'name',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        self.validate_unic(ingredients, tags)
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                {'cooking_time': 'Время приготовления должно быть больше 0'}
            )
        return data

    def validate_ingredients(self, ingredients):
        if len(ingredients) <= 0:
            raise serializers.ValidationError(
                'В рецепте должен быть хотя бы один ингредиент'
            )
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Колличество ингредиентов должно быть больше 0'
                )
        return ingredients

    def validate_tags(self, tags):
        if len(tags) <= 0:
            raise serializers.ValidationError(
                {'tags': 'Укажите хотя бы один тег в рецепте'}
            )
        return tags

    def validate_unic(self, ingredients, tags):
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиент должен быть уникальным'}
                )
            ingredients_list.append(ingredient)
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    {'tags': 'Тэг должен быть уникальным'}
                )
            tags_list.append(tag)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            IngredientMount.objects.create(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.tags.clear()
        tags = validated_data.get('tags')
        for tag in tags:
            instance.tags.add(tag)
        instance.recipe_ingredients.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredients')
        IngredientMount.objects.bulk_create(
            [IngredientMount(
                ingredient=ingredient['id'],
                recipe=instance,
                amount=ingredient['amount']
            ) for ingredient in ingredients
            ]
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerializer(
            instance, context=context
        ).data


class RecipeRepresentationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с моделью Recipe для представления response данных
    при POST запросах к моделям ShoppingCart, Favorite.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShoppingCartSerializer(serializers.ModelSerializer, CheckRequestMixin):
    """
    Сериализатор для работы с моделью ShoppingCart.
    """

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        request = self.context.get('request')
        self.good_request(request)
        recipe = data['recipe']
        if request.user.shopping_cart.filter(recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже в скиске покупок'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeRepresentationSerializer(
            instance.recipe, context=context
        ).data


class FavoriteSerializer(serializers.ModelSerializer, CheckRequestMixin):
    """
    Сериализатор для работы с моделью Favorite.
    """

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        request = self.context.get('request')
        self.good_request(request)
        recipe = data['recipe']
        if request.user.chooser.filter(recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'Рецепт уже есть в избранном'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeRepresentationSerializer(
            instance.recipe, context=context
        ).data
