from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from recipes.models import Ingredient, Tag, ShoppingCart, Recipe, \
    IngredientMount
from .serializers import (
    IngredientSerializer,
    TagSerializer,
    ShoppingCartSerializer, RecipeGetSerializer, RecipePostSerializer
)
from rest_framework.response import Response


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipePostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeGetSerializer(instance=serializer.instance)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class CartViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    model = ShoppingCart

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.model.objects.create(
            user=request.user, recipe=recipe)
        serializer = ShoppingCartSerializer()
        return Response(
            serializer.to_representation(instance=recipe),
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user = request.user
        recipe_id = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_cart = get_object_or_404(
            self.model,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def download(self, request):
        shopping_list = IngredientMount.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
                'ingredient__name').annotate(ingredient_total=Sum('amount'))

        content = (
            [f'{item["ingredient__name"]} ({item["ingredient__measurement_unit"]})'
            f'- {item["ingredient_total"]}\n'
            for item in shopping_list]
                   )
        filename = 'shopping_cart.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename={filename}'
        )
        return response
