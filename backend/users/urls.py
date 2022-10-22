from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import FollowViewSet

router = DefaultRouter()

router.register(
    prefix='subscriptions',
    viewset=FollowViewSet,
    basename='follows'
)

urlpatterns = [
    # path('users/', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
