from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Recipe, ShoppingCart
from rest_framework import status
from rest_framework.response import Response

from .serializers import FavoriteSerializer, ShoppingCartSerializer


class RecipePostDeleteMixin:
    """
    Миксин для создания и удаления рецептов в favorite или в shopping_cart.
    """

    def create_or_delete(self, request, pk, model):
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            if model == 'favorite':
                serializer = FavoriteSerializer(
                    data=data,
                    context={'request': request}
                )
            if model == 'shopping_cart':
                serializer = ShoppingCartSerializer(
                    data=data,
                    context={'request': request}
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if model == 'favorite':
            obj = get_object_or_404(
                Favorite, user=user, recipe=recipe
            )
        if model == 'shopping_cart':
            obj = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
