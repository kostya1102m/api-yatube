from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import api_posts, api_posts_detail

urlpatterns = [
    path('api/v1/posts/', api_posts),
    path('api/v1/posts/<int:pk>/', api_posts_detail),
    path('api/v1/api-token-auth/', obtain_auth_token)
]