from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_V1 = routers.DefaultRouter()
router_V1.register('posts', PostViewSet, basename='posts')
router_V1.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)
router_V1.register('groups', GroupViewSet, basename='groups')
router_V1.register('follow', FollowViewSet, basename='followings')

urlpatterns = [
    path('v1/', include(router_V1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
