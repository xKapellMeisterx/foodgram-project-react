from django.contrib import admin

from .models import Ingredient, Recipe, Tag, ShoppingCart


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'hexcolor',
        'slug'
    )


@admin.register(Ingredient)
class Ingredients(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
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
