from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet, TokenObtainView, UserRegistrationView

app_name = 'api'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')

comments_router = SimpleRouter()
comments_router.register(
    r'comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    # path(
    #     'v1/register/',
    #     UserRegistrationView.as_view(),
    #     name='register',
    # ),
    # path(
    #     'v1/login/', 
    #     TokenObtainView.as_view(), 
    #     name='login'
    # ),
    path('v1/', include(router.urls)),
    path(
        'v1/posts/<int:post_id>/',
        include(comments_router.urls),
    ),
]