from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from drf_spectacular.utils import extend_schema
from posts.models import Post, Group
from .serializers import UserSerializer
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model

from .hateoas_serializer import (
    PostDetailSerializer,
    PostListSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
    GroupSerializer,
    FollowSerializer
)

from .actions import Actions as user_actions


User = get_user_model()
    
@extend_schema(tags=['Posts'])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'group')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action == user_actions.RETRIEVE:
            return PostDetailSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=['Groups'])
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@extend_schema(tags=['Post Comments'])
class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action == user_actions.RETRIEVE:
            return CommentDetailSerializer
        return CommentListSerializer
    
    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.select_related('author', 'post')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post(),
        )

class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
): ...


@extend_schema(tags=['Follow'])
class FollowViewSet(CreateListViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return self.request.user.follower.select_related('user', 'following')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'