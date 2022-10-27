from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import FollowViewSet

router = DefaultRouter()
router.register('follow', FollowViewSet, basename='follows')

urlpatterns = [
    # path('users/subscriptions/', FollowViewSet.as_view,
    #      name='subscription'),
    # path('users/<int:id>/subscribe/', FollowViewSet.as_view(),
    #      name='subscribe'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
