from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsModelViewSet, RecipeModelViewSet,
                    TagsModelViewSet)

router = DefaultRouter()
router.register('tags', TagsModelViewSet, basename='tags')
router.register('ingredients', IngredientsModelViewSet, basename='ingredients')
router.register('recipes', RecipeModelViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
