from api.pagination import NewPageNumberPagination
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Follow, User
from users.serializers import FollowListSerializer, FollowSerializer


class FollowApiView(APIView):
    """
    Работа с данными модели Follow.
    Формирует представление данных при POST, DEL запросах
    к endpoint:
    /api/users/{id}/subscribe/
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = get_object_or_404(
            Follow, user=user, following=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListApiView(ListAPIView):
    """
    Работа с данными модели Follow.
    Формирует представление данных при GET запросах
    к endpoint:
    /api/users/subscriptions/
    """

    permission_classes = (IsAuthenticated,)
    pagination_class = NewPageNumberPagination

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
