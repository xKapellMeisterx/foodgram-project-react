from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientMount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'hexcolor',
        'slug'
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'cooking_time',
    )
    list_filter = ('tags',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(Favorite)
class FavoriteCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(IngredientMount)
class IngredientMountAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount'
    )


