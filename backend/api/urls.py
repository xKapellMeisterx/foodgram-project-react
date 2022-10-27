from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, TagsViewSet, CartViewSet

router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

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
]


