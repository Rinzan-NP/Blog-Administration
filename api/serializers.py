from rest_framework import serializers
from .models import BlogPost, Author, Tag, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class HealthCheckSerializer(serializers.Serializer):
    """Serializer for health check endpoint"""
    status = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""
    author_id = serializers.UUIDField(source='author.id', read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    created_by_id = serializers.UUIDField(source='created_by.id', read_only=True, allow_null=True)
    updated_by_id = serializers.UUIDField(source='updated_by.id', read_only=True, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of tag names to associate with the blog post"
    )

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'subtitle',
            'content',
            'author_id',
            'author_name',
            'category',
            'tags',
            'tag_names',
            'featured_image',
            'meta_title',
            'meta_description',
            'status',
            'published_at',
            'comments_enabled',
            'featured',
            'created_at',
            'updated_at',
            'created_by_id',
            'updated_by_id',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_slug(self, value):
        """Ensure slug is unique"""
        if self.instance and self.instance.slug == value:
            return value
        if BlogPost.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A blog post with this slug already exists.")
        return value

    def create(self, validated_data):
        """Create a new blog post with tags"""
        tag_names = validated_data.pop('tag_names', [])
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        
        instance = super().create(validated_data)
        
        # Handle tags
        if tag_names:
            tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name.strip(),
                    defaults={'slug': tag_name.strip().lower().replace(' ', '-')}
                )
                tag_objects.append(tag)
            instance.tags.set(tag_objects)
        
        return instance

    def update(self, instance, validated_data):
        """Update an existing blog post with tags"""
        tag_names = validated_data.pop('tag_names', None)
        request = self.context.get('request')
        if request and request.user:
            validated_data['updated_by'] = request.user
        
        instance = super().update(instance, validated_data)
        
        # Handle tags if provided
        if tag_names is not None:
            tag_objects = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name.strip(),
                    defaults={'slug': tag_name.strip().lower().replace(' ', '-')}
                )
                tag_objects.append(tag)
            instance.tags.set(tag_objects)
        
        return instance

    def create(self, validated_data):
        """Create a new blog post"""
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update an existing blog post"""
        request = self.context.get('request')
        if request and request.user:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


class BlogPostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for blog post lists"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'subtitle',
            'author_name',
            'category',
            'tags',
            'featured_image',
            'status',
            'published_at',
            'featured',
            'created_at',
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    blog_post_id = serializers.UUIDField(source='blog_post.id', read_only=True)
    blog_post_title = serializers.CharField(source='blog_post.title', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'blog_post_id',
            'blog_post_title',
            'name',
            'email',
            'content',
            'is_approved',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'is_approved', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Validate email format"""
        return value.lower().strip()

    def create(self, validated_data):
        """Create a new comment"""
        # Get blog_post from context (passed from view)
        blog_post = self.context.get('blog_post')
        if not blog_post:
            raise serializers.ValidationError("Blog post is required.")
        
        validated_data['blog_post'] = blog_post
        
        # Check if comments are enabled for this blog post
        if not blog_post.comments_enabled:
            raise serializers.ValidationError("Comments are disabled for this blog post.")
        
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating comments (simplified, no read-only fields)"""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']

    def validate_email(self, value):
        """Validate email format"""
        return value.lower().strip()

