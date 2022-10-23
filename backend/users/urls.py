from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import FollowViewSet


urlpatterns = [
    # path('users/<int:id>/subscribe/', FollowViewSet.as_view(),
    #      name='subscribe'),
    # path('users/subscriptions/', FollowViewSet.as_view,
    #      name='subscription'),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
