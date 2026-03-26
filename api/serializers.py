from rest_framework import serializers

from posts.models import Post, Group, Comment

from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        read_only_fields = ('author',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')


# class UserRegisterSerializer(serializers.Serializer):

#     username = serializers.CharField(
#         required=True,
#         min_length=3,
#         max_length=20,
#     )
#     email = serializers.EmailField(required=False)
#     password = serializers.CharField(
#         required=True,
#         write_only=True,
#         min_length=8,
#         style={'input_type': 'password'},
#     )

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError(
#                 'Пользователь с таким username уже существует.'
#             )
#         return value

#     def validate_email(self, value):
#         if value and User.objects.filter(email=value).exists():
#             raise serializers.ValidationError(
#                 'Пользователь с таким email уже существует.'
#             )
#         return value

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)