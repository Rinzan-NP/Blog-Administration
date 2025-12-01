from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'posts', views.BlogPostViewSet, basename='blogpost')

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('posts/<uuid:post_id>/comments/', views.create_comment, name='create-comment'),
    path('posts/<uuid:post_id>/comments/list/', views.list_comments, name='list-comments'),
    path('', include(router.urls)),
]

