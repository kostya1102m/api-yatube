from rest_framework import serializers
from rest_framework.reverse import reverse
from posts.models import Post, Comment, Group, Follow
from django.contrib.auth import get_user_model

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
            'self': self.build_absolute_url('api:posts-detail', pk=obj.id),
            'comments': self.build_absolute_url(
                'api:comments-list', 
                post_id=obj.id
            ),
        }
        
        if obj.group:
            links['group'] = self.build_absolute_url(
                'api:groups-detail', 
                pk=obj.group.id
            )

        #TODO(линки автора после добавления UserViewSet)
        
        return {k: v for k, v in links.items() if v is not None}