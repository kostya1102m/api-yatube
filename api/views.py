from django.shortcuts import get_object_or_404
from rest_framework import viewsets, serializers, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from drf_spectacular.utils import extend_schema_view, inline_serializer, extend_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer, UserRegisterSerializer
from .permissions import IsAuthorOrReadOnly

class TokenObtainView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Auth'],
        request=AuthTokenSerializer,
        responses={
            200: inline_serializer(
                name='TokenResponse',
                fields={'token': serializers.CharField()},
            ),
        },
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
@extend_schema(tags=['Posts'])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(tags=['Groups'])
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Post Comments'])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post(),
        )


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Auth'],
        request=UserRegisterSerializer,
        responses={
            201: inline_serializer(
                name='RegistrationResponse',
                fields={
                    'id': serializers.IntegerField(),
                    'username': serializers.CharField(),
                    'email': serializers.CharField(),
                    # 'token': serializers.CharField(),
                },
            ),
        },
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # 'token': token.key,
            },
            status=status.HTTP_201_CREATED,
        )