from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CartViewSet, FavoriteViewSet, IngredientsViewSet,
                    RecipeViewSet, TagsViewSet)

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'recipes/download_shopping_cart/',
        CartViewSet.as_view({'get': 'download'}),
        name='download'
    ),
    path(
        'recipes/<recipes_id>/shopping_cart/',
        CartViewSet.as_view({'post': 'create', 'delete': 'delete'}),
        name='cart'
    ),
    path(
        'recipes/<recipes_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'create', 'delete': 'delete'}),
        name='favorite'
    ),
]


