import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(models.Model):
    """Author model for blog posts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Author's name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag model for blog posts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, help_text="Tag name")
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    content = models.JSONField(help_text="Blog post content in JSON format")
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        related_name='blog_posts',
        help_text="Author of the blog post"
    )
    category = models.CharField(max_length=100)
    tags = models.ManyToManyField(
        'Tag',
        related_name='blog_posts',
        blank=True,
        help_text="Tags for the blog post"
    )
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, help_text="Featured image for the blog post")
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    published_at = models.DateTimeField(blank=True, null=True)
   
    
    comments_enabled = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='blog_posts_created',
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='blog_posts_updated',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['published_at']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comment model for blog posts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog_post = models.ForeignKey(
        'BlogPost',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Blog post this comment belongs to"
    )
    name = models.CharField(max_length=255, help_text="Commenter's name")
    email = models.EmailField(help_text="Commenter's email")
    content = models.TextField(help_text="Comment content")
    is_approved = models.BooleanField(default=False, help_text="Whether the comment is approved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['blog_post', 'created_at']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.blog_post.title}"
