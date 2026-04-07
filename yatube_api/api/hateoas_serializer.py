from rest_framework import serializers
from rest_framework.reverse import reverse
from posts.models import Post, Comment, Group, Follow
from django.contrib.auth import get_user_model
from .actions import Actions as user_actions

User = get_user_model()


class HATEOASMixin:    
    def build_absolute_url(self, view_name, **kwargs):
        request = self.context.get('request')
        try:
            return reverse(view_name, kwargs=kwargs, request=request)
        except Exception:
            return None


class PostListSerializer(serializers.ModelSerializer, HATEOASMixin):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    _links = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date', '_links')
        read_only_fields = ('author',)
    
    def get__links(self, obj):
        links = {
            'self': self.build_absolute_url(
                'api:posts-detail', 
                pk=obj.id
            ),

            'comments': self.build_absolute_url(
                'api:comments-list', 
                post_id=obj.id
            ),

            'author': self.build_absolute_url(
                'api:users-detail', 
                username=obj.author.username
            ),
        }
        
        if obj.group:
            links['group'] = self.build_absolute_url(
                'api:groups-detail', 
                pk=obj.group.id
            )
        
        return {k: v for k, v in links.items() if v is not None}
    

class PostDetailSerializer(PostListSerializer):
    _actions = serializers.SerializerMethodField()
    
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ('_actions',)
    
    def get__actions(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        actions = []
        
        if user and user.is_authenticated and obj.author == user:
            base_url = self.build_absolute_url('api:posts-detail', pk=obj.id)
            
            actions.extend([
                {
                    'name': 'update',
                    'method': 'PUT',
                    'href': base_url,
                },
                {
                    'name': 'partial_update',
                    'method': 'PATCH',
                    'href': base_url,
                },
                {
                    'name': 'delete',
                    'method': 'DELETE',
                    'href': base_url,
                }
            ])
        
        if user and user.is_authenticated:
            actions.append({
                'name': 'create_comment',
                'method': 'POST',
                'href': self.build_absolute_url('api:comments-list', post_id=obj.id),
            })
        
        return actions


class CommentListSerializer(serializers.ModelSerializer, HATEOASMixin):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    _links = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created', '_links')
        read_only_fields = ('author', 'post')
    
    def get__links(self, obj):
        return {
            'self': self.build_absolute_url(
                'api:comments-detail',
                post_id=obj.post.id,
                pk=obj.id
            ),
            'post': self.build_absolute_url('api:posts-detail', pk=obj.post.id),
            'author': self.build_absolute_url('api:users-detail', username=obj.author.username),
        }


class CommentDetailSerializer(CommentListSerializer):
    _actions = serializers.SerializerMethodField()
    
    class Meta(CommentListSerializer.Meta):
        fields = CommentListSerializer.Meta.fields + ('_actions',)
    
    def get__actions(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        actions = []
        
        if user and user.is_authenticated and obj.author == user:
            base_url = self.build_absolute_url(
                'api:comments-detail',
                post_id=obj.post.id,
                pk=obj.id
            )
            
            actions.extend([
                {'name': 'update', 'method': 'PUT', 'href': base_url},
                {'name': 'partial_update', 'method': 'PATCH', 'href': base_url},
                {'name': 'delete', 'method': 'DELETE', 'href': base_url},
            ])
        
        return actions

class GroupSerializer(serializers.ModelSerializer, HATEOASMixin):
    _links = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', '_links')
    
    def get__links(self, obj):
        return {
            'self': self.build_absolute_url('api:groups-detail', pk=obj.id),
        }


class FollowSerializer(serializers.ModelSerializer, HATEOASMixin):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', 
        queryset=User.objects.all()
    )
    _links = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ('user', 'following', '_links')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя.',
            ),
        ]
    
    def get__links(self, obj):
        return {
            'user': self.build_absolute_url('api:users-detail', username=obj.user.username),
            'following': self.build_absolute_url('api:users-detail', username=obj.following.username),
        }
    
    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError('Нельзя подписаться на самого себя.')
        return value


class UserSerializer(serializers.ModelSerializer, HATEOASMixin):
    _links = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', '_links')
        read_only_fields = ('id', 'username')
    
    def get__links(self, obj):
        return {
            'self': self.build_absolute_url('api:users-detail', username=obj.username),
        }