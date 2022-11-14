from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from recipes.models import (Ingredient, IngredientMount, Recipe, ShoppingCart,
                            Tag, Favorite)
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeGetSerializer,
                          RecipePostSerializer, ShoppingCartSerializer,
                          TagSerializer, FavoriteSerializer)


class TagsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class IngredientsViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Ingredient.objects.all()
        serializer = IngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Ingredient.objects.all()
        ingredient = get_object_or_404(queryset, pk=pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ViewSet, CreateModelMixin, UpdateModelMixin):

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request):
        queryset = Recipe.objects.all()
        serializer = RecipeGetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = RecipePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeGetSerializer(instance=serializer.instance)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = Recipe.objects.all()
        ingredient = get_object_or_404(queryset, pk=pk)
        serializer = RecipeGetSerializer(ingredient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Recipe.objects.get(pk=kwargs.get('pk'))
        serializer = RecipePostSerializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RecipeGetSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
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
            user=request.user,
            recipe=recipe
        )
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


class FavoriteViewSet(viewsets.ViewSet):

    def create(self, request, recipes_id):
        data = {'user': request.user.id, 'recipe': recipes_id}
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipes_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipes_id)
        favorite = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)