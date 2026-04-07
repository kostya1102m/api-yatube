from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import FollowViewSet, PostViewSet, GroupViewSet, CommentViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follows', FollowViewSet, basename='follow')
router.register(r'users', UserViewSet, basename='users')

comments_router = SimpleRouter()
comments_router.register(
    r'comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/posts/<int:post_id>/',
        include(comments_router.urls),
    ),
]