from django.contrib import admin

from .models import Ingredients, Recipes, Tag


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'hexcolor',
        'slug'
    )


@admin.register(Ingredients)
class Ingredients(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'cooking_time'
    )
    list_filter = ('tags',)
