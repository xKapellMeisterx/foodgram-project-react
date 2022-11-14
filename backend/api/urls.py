from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ShoppingCartViewSet, FavoriteViewSet, IngredientsViewSet,
                    RecipeViewSet, TagsViewSet)

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        ShoppingCartViewSet.as_view({'get': 'download'}),
        name='download_shopping_cart'
    ),
    path('', include(router.urls)),
    path(
        'recipes/<recipes_id>/shopping_cart/',
        ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='cart'
    ),
    path(
        'recipes/<recipes_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='favorite'
    ),
]
