from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from recipes.models import (Favorite, Ingredient, IngredientMount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipePostSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagsModelViewSet(viewsets.ModelViewSet):
    """
    Работа с данными модели Tags.
    Формирует представление данных при GET запросах к следующим endpoints:
    /api/tags/
    /api/tags/{id}/
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
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
    http_method_names = ('get',)


class RecipeModelViewSet(viewsets.ModelViewSet):
    """
    Работа с данными модели Recipe.
    Формирует представление данных при GET, POST, PATH, DEL запросах
    к следующим endpoints:
    /api/recipes/
    /api/recipes/{id}/
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

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
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                Favorite, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = ShoppingCartSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                ShoppingCart,
                user=user,
                recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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
        ).values(
            name=F('ingredient__name'),
            measurement_unit=F('ingredient__measurement_unit')
        ).annotate(ingredient_total=Sum('amount'))
        content = (
            [f'{item["name"]} ({item["measurement_unit"]}) - '
             f'{item["ingredient_total"]}\n' for item in shopping_list]
        )
        filename = 'shopping_cart.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename={filename}'
        )
        return response
