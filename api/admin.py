from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import BlogPost, Author, Tag, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model"""
    list_display = ['name', 'blog_posts_count', 'created_at', 'updated_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'blog_posts_count']
    list_per_page = 25
    fieldsets = (
        ('Author Information', {
            'fields': ('id', 'name'),
            'description': 'Enter the author\'s name. This will be displayed on blog posts.'
        }),
        ('Statistics', {
            'fields': ('blog_posts_count',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def blog_posts_count(self, obj):
        """Display the number of blog posts by this author"""
        count = obj.blog_posts.count()
        if count > 0:
            url = reverse('admin:api_blogpost_changelist') + f'?author__id__exact={obj.id}'
            return format_html('<a href="{}">{} post{}</a>', url, count, 's' if count != 1 else '')
        return '0 posts'
    blog_posts_count.short_description = 'Blog Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model"""
    list_display = ['name', 'slug', 'blog_posts_count', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'blog_posts_count']
    list_per_page = 25
    fieldsets = (
        ('Tag Information', {
            'fields': ('id', 'name', 'slug'),
            'description': 'Tags help organize and categorize blog posts. The slug is automatically generated from the name.'
        }),
        ('Statistics', {
            'fields': ('blog_posts_count',),
            'classes': ('collapse',)
        }),
    )

    def blog_posts_count(self, obj):
        """Display the number of blog posts with this tag"""
        count = obj.blog_posts.count()
        if count > 0:
            url = reverse('admin:api_blogpost_changelist') + f'?tags__id__exact={obj.id}'
            return format_html('<a href="{}">{} post{}</a>', url, count, 's' if count != 1 else '')
        return '0 posts'
    blog_posts_count.short_description = 'Blog Posts'


class CommentInline(admin.TabularInline):
    """Inline comments for blog posts"""
    model = Comment
    extra = 0
    readonly_fields = ['name', 'email', 'content', 'created_at', 'is_approved']
    fields = ['name', 'email', 'content', 'is_approved', 'created_at']
    can_delete = False
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""
    list_display = ['name', 'email', 'blog_post_link', 'content_preview', 'is_approved_badge', 'created_at']
    list_filter = ['is_approved', 'created_at', 'blog_post']
    search_fields = ['name', 'email', 'content', 'blog_post__title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_per_page = 50
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Comment Information', {
            'fields': ('id', 'blog_post', 'name', 'email', 'content'),
            'description': 'Review and moderate comments from readers.'
        }),
        ('Moderation', {
            'fields': ('is_approved',),
            'description': 'Only approved comments will be visible on the website.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['approve_comments', 'disapprove_comments', 'delete_selected']

    def blog_post_link(self, obj):
        """Link to the blog post"""
        if obj.blog_post:
            url = reverse('admin:api_blogpost_change', args=[obj.blog_post.pk])
            return format_html('<a href="{}">{}</a>', url, obj.blog_post.title)
        return '-'
    blog_post_link.short_description = 'Blog Post'
    blog_post_link.admin_order_field = 'blog_post__title'

    def content_preview(self, obj):
        """Show a preview of the comment content"""
        if len(obj.content) > 100:
            return format_html('{}...', obj.content[:100])
        return obj.content
    content_preview.short_description = 'Content Preview'

    def is_approved_badge(self, obj):
        """Display approval status with badge"""
        if obj.is_approved:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">✓ Approved</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">✗ Pending</span>'
        )
    is_approved_badge.short_description = 'Status'
    is_approved_badge.admin_order_field = 'is_approved'

    def approve_comments(self, request, queryset):
        """Approve selected comments"""
        count = queryset.update(is_approved=True)
        self.message_user(request, f'Successfully approved {count} comment{"" if count == 1 else "s"}.', level='success')
    approve_comments.short_description = '✓ Approve selected comments'

    def disapprove_comments(self, request, queryset):
        """Disapprove selected comments"""
        count = queryset.update(is_approved=False)
        self.message_user(request, f'Successfully disapproved {count} comment{"" if count == 1 else "s"}.', level='warning')
    disapprove_comments.short_description = '✗ Disapprove selected comments'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface for BlogPost model"""
    list_display = [
        'title_preview',
        'author',
        'category',
        'status_badge',
        'featured_badge',
        'comments_count',
        'tags_display',
        'published_at',
        'created_at',
    ]
    list_filter = [
        'status',
        'category',
        'featured',
        'comments_enabled',
        'author',
        'tags',
        'created_at',
        'published_at',
    ]
    search_fields = [
        'title',
        'slug',
        'subtitle',
        'category',
        'author__name',
        'tags__name',
    ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'comments_count',
        'featured_image_preview',
    ]
    filter_horizontal = ['tags']
    autocomplete_fields = ['author']
    date_hierarchy = 'published_at'
    list_per_page = 25
    list_select_related = ['author']
    inlines = [CommentInline]
    save_on_top = True
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'slug', 'subtitle', 'author', 'category', 'tags'),
            'description': 'Enter the basic information for your blog post. The slug will be automatically generated from the title.'
        }),
        ('Content', {
            'fields': ('content', 'featured_image', 'featured_image_preview'),
            'description': 'Add your blog post content and featured image.'
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
            'description': 'SEO metadata for search engines. Leave blank to use defaults.'
        }),
        ('Status & Publishing', {
            'fields': ('status', 'published_at', 'featured', 'comments_enabled'),
            'description': 'Control the visibility and features of your blog post.'
        }),
        ('Statistics', {
            'fields': ('comments_count',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['make_published', 'make_draft', 'make_featured', 'unfeature']

    def title_preview(self, obj):
        """Display title with link"""
        url = reverse('admin:api_blogpost_change', args=[obj.pk])
        return format_html('<a href="{}"><strong>{}</strong></a>', url, obj.title)
    title_preview.short_description = 'Title'
    title_preview.admin_order_field = 'title'

    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'published': '#28a745',
            'draft': '#ffc107',
            'archived': '#6c757d'
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; text-transform: uppercase;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def featured_badge(self, obj):
        """Display featured status"""
        if obj.featured:
            return format_html(
                '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">⭐ Featured</span>'
            )
        return '-'
    featured_badge.short_description = 'Featured'
    featured_badge.admin_order_field = 'featured'

    def tags_display(self, obj):
        """Display tags as badges"""
        tags = obj.tags.all()
        if tags:
            tag_html = []
            for tag in tags[:5]:  # Show first 5 tags
                tag_html.append(
                    format_html(
                        '<span style="background-color: #e9ecef; color: #495057; padding: 2px 6px; border-radius: 3px; font-size: 10px; margin-right: 3px;">{}</span>',
                        tag.name
                    )
                )
            if tags.count() > 5:
                tag_html.append(format_html('<span style="color: #6c757d;">+{} more</span>', tags.count() - 5))
            return format_html(''.join(tag_html))
        return '-'
    tags_display.short_description = 'Tags'

    def comments_count(self, obj):
        """Display number of comments"""
        count = obj.comments.count()
        approved_count = obj.comments.filter(is_approved=True).count()
        if count > 0:
            url = reverse('admin:api_comment_changelist') + f'?blog_post__id__exact={obj.id}'
            return format_html(
                '<a href="{}">{} total ({} approved)</a>',
                url, count, approved_count
            )
        return '0 comments'
    comments_count.short_description = 'Comments'

    def featured_image_preview(self, obj):
        """Display featured image preview"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 5px;" />',
                obj.featured_image.url
            )
        return 'No image uploaded'
    featured_image_preview.short_description = 'Image Preview'

    def make_published(self, request, queryset):
        """Mark selected posts as published"""
        count = queryset.update(status='published')
        self.message_user(request, f'Successfully published {count} post{"" if count == 1 else "s"}.', level='success')
    make_published.short_description = '📝 Mark as published'

    def make_draft(self, request, queryset):
        """Mark selected posts as draft"""
        count = queryset.update(status='draft')
        self.message_user(request, f'Successfully marked {count} post{"" if count == 1 else "s"} as draft.', level='info')
    make_draft.short_description = '📄 Mark as draft'

    def make_featured(self, request, queryset):
        """Mark selected posts as featured"""
        count = queryset.update(featured=True)
        self.message_user(request, f'Successfully featured {count} post{"" if count == 1 else "s"}.', level='success')
    make_featured.short_description = '⭐ Mark as featured'

    def unfeature(self, request, queryset):
        """Unfeature selected posts"""
        count = queryset.update(featured=False)
        self.message_user(request, f'Successfully unfeatured {count} post{"" if count == 1 else "s"}.', level='info')
    unfeature.short_description = 'Remove featured status'

    def save_model(self, request, obj, form, change):
        """Set created_by and updated_by automatically"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
