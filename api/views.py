from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import BlogPost, Comment
from .serializers import (
    HealthCheckSerializer, 
    BlogPostSerializer, 
    BlogPostListSerializer,
    CommentSerializer,
    CommentCreateSerializer
)


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint to verify API is running
    """
    serializer = HealthCheckSerializer({
        'status': 'healthy',
        'message': 'Django REST Framework API is running successfully!'
    })
    return Response(serializer.data, status=status.HTTP_200_OK)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for viewing BlogPost instances.
    Posts can only be created/updated via Django Admin.
    
    list: Return a paginated list of all blog posts (GET /api/posts/)
    retrieve: Return a specific blog post by ID (GET /api/posts/{id}/)
    
    Query parameters:
    - author: Filter by author UUID (e.g., ?author=uuid)
    - status: Filter by status (draft|published|archived)
    - category: Filter by category
    - featured: Filter by featured (true|false)
    - search: Search in title, subtitle, category
    - ordering: Order by created_at, updated_at, published_at
    """
    queryset = BlogPost.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'subtitle', 'category']
    ordering_fields = ['created_at', 'updated_at', 'published_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer

    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by author if provided
        author_filter = self.request.query_params.get('author', None)
        if author_filter:
            queryset = queryset.filter(author_id=author_filter)
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by category if provided
        category_filter = self.request.query_params.get('category', None)
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        
        # Filter by featured if provided
        featured_filter = self.request.query_params.get('featured', None)
        if featured_filter is not None:
            featured_bool = featured_filter.lower() == 'true'
            queryset = queryset.filter(featured=featured_bool)
        
        # Only show published posts by default for non-authenticated users
        # (This can be overridden by explicitly passing status parameter)
        if not self.request.user.is_authenticated and not status_filter:
            queryset = queryset.filter(status='published')
        
        return queryset


@api_view(['POST'])
def create_comment(request, post_id):
    """
    Create a new comment for a blog post.
    
    POST /api/posts/{post_id}/comments/
    
    Request body:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "content": "Great post!"
    }
    """
    # Get the blog post
    blog_post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if comments are enabled
    if not blog_post.comments_enabled:
        return Response(
            {'error': 'Comments are disabled for this blog post.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Serialize and validate the comment data
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Create the comment
        comment = serializer.save(blog_post=blog_post)
        
        # Return the full comment data
        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_comments(request, post_id):
    """
    Get all approved comments for a blog post.
    
    GET /api/posts/{post_id}/comments/
    """
    blog_post = get_object_or_404(BlogPost, id=post_id)
    
    # Get only approved comments
    comments = Comment.objects.filter(blog_post=blog_post, is_approved=True)
    serializer = CommentSerializer(comments, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
