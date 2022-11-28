from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, IngredientMount, Recipe, Tag
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .filters import IngredientSearchFilter, RecipeFilter
from .mixins import RecipePostDeleteMixin
from .pagination import NewPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeGetSerializer,
                          RecipePostSerializer, TagSerializer)


class TagsModelViewSet(viewsets.ModelViewSet):
    """
    Работа с данными модели Tags.
    Формирует представление данных при GET запросах к следующим endpoints:
    /api/tags/
    /api/tags/{id}/
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ('get', )


class IngredientsModelViewSet(viewsets.ModelViewSet):
    """
    Работа с данными модели Ingredients.
    Формирует представление данных при GET запросах к следующим endpoints:
    /api/ingredients/
    /api/ingredients/{id}/
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
    http_method_names = ('get',)


class RecipeModelViewSet(viewsets.ModelViewSet, RecipePostDeleteMixin):
    """
    Работа с данными модели Recipe.
    Формирует представление данных при GET, POST, PATH, DEL запросах
    к следующим endpoints:
    /api/recipes/
    /api/recipes/{id}/
    """

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = NewPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'get':
            return RecipeGetSerializer
        return RecipePostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """
        Работа с данными модели Favorite.
        Формирует представление данных при POST, DEL запросах
        к endpoint:
        /api/recipes/{id}/favorite/
        """

        return self.create_or_delete(request, pk, model='favorite')

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """
        Работа с данными модели ShoppingCart.
        Формирует представление данных при POST, DEL запросах
        к endpoint:
        /api/recipes/{id}/shopping_cart/
        """

        return self.create_or_delete(request, pk, model='shopping_cart')

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """
        Скачивает файл со список покупок необходимых для приготовления всех
        рецептов в формате TXT при GET запросе к endpoint:
        /api/recipes/download_shopping_cart/
        """

        shopping_list = IngredientMount.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(
            ingredient_total=Sum('amount')
        )
        content = (
            [f'{item[0]} ({item[1]}) - {item[2]}\n' for item in shopping_list]
        )
        filename = 'shopping_cart.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename={filename}'
        )
        return response
