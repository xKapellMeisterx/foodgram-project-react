from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.validators import UniqueTogetherValidator

from users.mixins import GetIsFollowMixin, CheckRequestMixin
from users.models import Follow, User


# class CheckRequestMixin:
#     """Миксин для проверки запроса."""
#
#     def good_request(self, request):
#         if not request or request.user.is_anonymous:
#             return False
#
#
# class GetIsFollowMixin:
#     """
#     Миксин проверяет запрос. После этого проверяет подписал ли пользователь
#     на автора.
#     """
#
#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         if not request or request.user.is_anonymous:
#             return False
#         return request.user.follower.filter(following=obj).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для работы с моделью User."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer, GetIsFollowMixin):
    """Сериализатор для работы с моделью User включая вывод подписок."""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    pagination_class = LimitOffsetPagination

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class FollowRecipesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления данных о рецептах,
    которые созданы пользователем.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FollowSerializer(serializers.ModelSerializer, CheckRequestMixin):
    """Сериализатор работы с моделью Follow."""

    class Meta:
        model = Follow
        fields = (
            'user',
            'following'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Вы уже подписаны на данного пользователя!')
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        self.good_request(request)
        following = data['following']
        if request.user == following:
            raise serializers.ValidationError(
                'Вы не можете подписаться на себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowListSerializer(
            instance.following, context=context
        ).data


class FollowListSerializer(
    serializers.ModelSerializer, GetIsFollowMixin, CheckRequestMixin
):
    """Сериализатор для получения списка подписок."""

    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        self.good_request(request)
        context = {'request': request}
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = (obj.recipes.all()[:int(recipes_limit)]
                   if recipes_limit else obj.recipes.all())
        return FollowRecipesSerializer(
            recipes, many=True, context=context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
