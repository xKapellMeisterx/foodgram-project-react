from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import Follow, User
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import FollowSerializer


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class FollowListApiView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         queryset = User.objects.filter(following__user=user)
#         serializer = FollowSerializer


