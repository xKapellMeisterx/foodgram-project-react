from django.urls import include, path, re_path
from users.views import FollowApiView, FollowListApiView

urlpatterns = [
    path('users/subscriptions/', FollowListApiView.as_view(),
         name='subscription'),
    path('users/<int:id>/subscribe/', FollowApiView.as_view(),
         name='subscribe'),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
