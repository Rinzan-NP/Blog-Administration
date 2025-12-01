# Blog API Documentation

## Base URL

```
http://your-domain.com/api/
```

## Authentication

Currently, all endpoints are publicly accessible (AllowAny permission). Blog posts can only be created/updated via Django Admin.

---

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /api/health/`

**Response:**
```json
{
    "status": "healthy",
    "message": "Django REST Framework API is running successfully!"
}
```

**Status Code:** `200 OK`

---

### 2. List Blog Posts

Retrieve a paginated list of blog posts.

**Endpoint:** `GET /api/posts/`

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `author` | UUID | Filter by author UUID | `?author=123e4567-e89b-12d3-a456-426614174000` |
| `status` | string | Filter by status (`draft`, `published`, `archived`) | `?status=published` |
| `category` | string | Filter by category | `?category=technology` |
| `featured` | boolean | Filter by featured status | `?featured=true` |
| `search` | string | Search in title, subtitle, category | `?search=django` |
| `ordering` | string | Order results (`created_at`, `updated_at`, `published_at`) | `?ordering=-created_at` |
| `page` | integer | Page number for pagination | `?page=2` |

**Note:** By default, only published posts are shown to non-authenticated users. You can override this by explicitly passing the `status` parameter.

**Response:**
```json
{
    "count": 10,
    "next": "http://your-domain.com/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Getting Started with Django",
            "slug": "getting-started-with-django",
            "subtitle": "A comprehensive guide",
            "author_name": "John Doe",
            "category": "Technology",
            "tags": [
                {
                    "id": "456e7890-e89b-12d3-a456-426614174001",
                    "name": "Django",
                    "slug": "django"
                },
                {
                    "id": "789e0123-e89b-12d3-a456-426614174002",
                    "name": "Python",
                    "slug": "python"
                }
            ],
            "featured_image": "http://your-domain.com/media/blog_images/image.jpg",
            "status": "published",
            "published_at": "2024-01-15T10:30:00Z",
            "featured": true,
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
}
```

**Status Code:** `200 OK`

**Pagination:** Results are paginated with 10 items per page by default.

---

### 3. Retrieve Blog Post

Get detailed information about a specific blog post.

**Endpoint:** `GET /api/posts/{id}/`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Blog post UUID |

**Response:**
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Getting Started with Django",
    "slug": "getting-started-with-django",
    "subtitle": "A comprehensive guide",
    "content": {
        "blocks": [
            {
                "type": "paragraph",
                "data": {
                    "text": "This is the content..."
                }
            }
        ]
    },
    "author_id": "789e0123-e89b-12d3-a456-426614174003",
    "author_name": "John Doe",
    "category": "Technology",
    "tags": [
        {
            "id": "456e7890-e89b-12d3-a456-426614174001",
            "name": "Django",
            "slug": "django"
        }
    ],
    "featured_image": "http://your-domain.com/media/blog_images/image.jpg",
    "meta_title": "Getting Started with Django - Blog",
    "meta_description": "Learn how to get started with Django framework",
    "status": "published",
    "published_at": "2024-01-15T10:30:00Z",
    "comments_enabled": true,
    "featured": true,
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "created_by_id": "abc12345-e89b-12d3-a456-426614174004",
    "updated_by_id": "abc12345-e89b-12d3-a456-426614174004"
}
```

**Status Code:** `200 OK`

**Error Response:**
```json
{
    "detail": "Not found."
}
```

**Status Code:** `404 Not Found`

---

### 4. Create Comment

Create a new comment for a blog post.

**Endpoint:** `POST /api/posts/{post_id}/comments/`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `post_id` | UUID | Blog post UUID |

**Request Body:**
```json
{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "content": "Great article! Very helpful."
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Commenter's name |
| `email` | string | Yes | Commenter's email address |
| `content` | string | Yes | Comment content |

**Response:**
```json
{
    "id": "def45678-e89b-12d3-a456-426614174005",
    "blog_post_id": "123e4567-e89b-12d3-a456-426614174000",
    "blog_post_title": "Getting Started with Django",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "content": "Great article! Very helpful.",
    "is_approved": false,
    "created_at": "2024-01-16T14:30:00Z",
    "updated_at": "2024-01-16T14:30:00Z"
}
```

**Status Code:** `201 Created`

**Error Responses:**

**Comments Disabled:**
```json
{
    "error": "Comments are disabled for this blog post."
}
```

**Status Code:** `400 Bad Request`

**Validation Error:**
```json
{
    "name": ["This field is required."],
    "email": ["Enter a valid email address."],
    "content": ["This field is required."]
}
```

**Status Code:** `400 Bad Request`

**Blog Post Not Found:**
```json
{
    "detail": "Not found."
}
```

**Status Code:** `404 Not Found`

**Note:** New comments are created with `is_approved: false` by default. They need to be approved by an admin before appearing in the comments list.

---

### 5. List Comments

Get all approved comments for a blog post.

**Endpoint:** `GET /api/posts/{post_id}/comments/list/`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `post_id` | UUID | Blog post UUID |

**Response:**
```json
[
    {
        "id": "def45678-e89b-12d3-a456-426614174005",
        "blog_post_id": "123e4567-e89b-12d3-a456-426614174000",
        "blog_post_title": "Getting Started with Django",
        "name": "Jane Smith",
        "email": "jane@example.com",
        "content": "Great article! Very helpful.",
        "is_approved": true,
        "created_at": "2024-01-16T14:30:00Z",
        "updated_at": "2024-01-16T14:30:00Z"
    },
    {
        "id": "ghi78901-e89b-12d3-a456-426614174006",
        "blog_post_id": "123e4567-e89b-12d3-a456-426614174000",
        "blog_post_title": "Getting Started with Django",
        "name": "Bob Johnson",
        "email": "bob@example.com",
        "content": "Thanks for sharing!",
        "is_approved": true,
        "created_at": "2024-01-16T15:00:00Z",
        "updated_at": "2024-01-16T15:00:00Z"
    }
]
```

**Status Code:** `200 OK`

**Note:** Only approved comments are returned. Comments are ordered by `created_at` in descending order (newest first).

**Error Response:**
```json
{
    "detail": "Not found."
}
```

**Status Code:** `404 Not Found`

---

## Data Models

### Blog Post

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `title` | string | Blog post title |
| `slug` | string | URL-friendly identifier (unique) |
| `subtitle` | string | Optional subtitle |
| `content` | JSON | Blog post content in JSON format |
| `author_id` | UUID | Author UUID |
| `author_name` | string | Author name |
| `category` | string | Post category |
| `tags` | array | Array of tag objects |
| `featured_image` | string | URL to featured image |
| `meta_title` | string | SEO meta title |
| `meta_description` | string | SEO meta description |
| `status` | string | Post status: `draft`, `published`, `archived` |
| `published_at` | datetime | Publication date/time |
| `comments_enabled` | boolean | Whether comments are enabled |
| `featured` | boolean | Whether post is featured |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

### Tag

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `name` | string | Tag name |
| `slug` | string | URL-friendly identifier |

### Comment

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique identifier |
| `blog_post_id` | UUID | Associated blog post UUID |
| `blog_post_title` | string | Blog post title |
| `name` | string | Commenter's name |
| `email` | string | Commenter's email |
| `content` | string | Comment content |
| `is_approved` | boolean | Approval status |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

---

## Example Requests

### cURL Examples

**Health Check:**
```bash
curl -X GET http://your-domain.com/api/health/
```

**List Blog Posts:**
```bash
curl -X GET "http://your-domain.com/api/posts/?status=published&category=technology"
```

**Get Blog Post:**
```bash
curl -X GET http://your-domain.com/api/posts/123e4567-e89b-12d3-a456-426614174000/
```

**Create Comment:**
```bash
curl -X POST http://your-domain.com/api/posts/123e4567-e89b-12d3-a456-426614174000/comments/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "content": "Great article!"
  }'
```

**List Comments:**
```bash
curl -X GET http://your-domain.com/api/posts/123e4567-e89b-12d3-a456-426614174000/comments/list/
```

### JavaScript (Fetch) Examples

**List Blog Posts:**
```javascript
fetch('http://your-domain.com/api/posts/?status=published')
  .then(response => response.json())
  .then(data => console.log(data));
```

**Create Comment:**
```javascript
fetch('http://your-domain.com/api/posts/123e4567-e89b-12d3-a456-426614174000/comments/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Jane Smith',
    email: 'jane@example.com',
    content: 'Great article!'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python (requests) Examples

**List Blog Posts:**
```python
import requests

response = requests.get('http://your-domain.com/api/posts/', params={
    'status': 'published',
    'category': 'technology'
})
data = response.json()
print(data)
```

**Create Comment:**
```python
import requests

response = requests.post(
    'http://your-domain.com/api/posts/123e4567-e89b-12d3-a456-426614174000/comments/',
    json={
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'content': 'Great article!'
    }
)
data = response.json()
print(data)
```

---

## Error Handling

The API uses standard HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| `200` | OK - Request successful |
| `201` | Created - Resource created successfully |
| `400` | Bad Request - Invalid request data |
| `404` | Not Found - Resource not found |
| `500` | Internal Server Error - Server error |

Error responses follow this format:
```json
{
    "field_name": ["Error message"],
    "detail": "Error message"
}
```

---

## Pagination

List endpoints use pagination with the following structure:

```json
{
    "count": 100,
    "next": "http://your-domain.com/api/posts/?page=2",
    "previous": null,
    "results": [...]
}
```

**Pagination Parameters:**
- `page` - Page number (default: 1)
- Page size: 10 items per page (default)

---

## Media Files

Featured images are served at:
```
http://your-domain.com/media/blog_images/{filename}
```

Make sure to include the full URL when displaying images in your application.

---

## Notes

1. **Comments Moderation:** All new comments require admin approval before they appear in the comments list. The `is_approved` field is set to `false` by default.

2. **Blog Post Creation:** Blog posts can only be created/updated via Django Admin interface, not through the API.

3. **Status Filtering:** By default, only published posts are shown to non-authenticated users. To see draft or archived posts, explicitly pass the `status` parameter.

4. **Tags:** Tags are automatically created if they don't exist when associating them with blog posts. Tag slugs are automatically generated from tag names.

5. **Image Upload:** Featured images are uploaded via Django Admin. The API returns the full URL to the image.

---

## Django Admin Interface

The Django Admin interface provides a user-friendly way to manage blog content, authors, tags, and comments. All blog posts must be created and edited through the admin interface.

### Accessing the Admin

**URL:** `http://your-domain.com/admin/`

**Login Required:** Yes - You need staff/superuser credentials to access the admin interface.

### Admin Features

The admin interface includes the following sections:

#### 1. Blog Posts Management

**Location:** `/admin/api/blogpost/`

**Features:**
- **List View:**
  - Visual status badges (Published/Draft/Archived)
  - Featured badge indicator
  - Clickable titles for quick editing
  - Tag badges display
  - Comments count with link
  - Author, category, and publication date display
  - Search functionality (title, slug, subtitle, category, author, tags)
  - Advanced filtering (status, category, featured, comments enabled, author, tags, dates)
  - Date hierarchy for easy navigation by publication date

- **Edit/Create View:**
  - **Basic Information:** Title, slug (auto-generated), subtitle, author (with autocomplete), category, tags (horizontal filter widget)
  - **Content:** JSON content editor, featured image upload with preview
  - **SEO Settings:** Meta title and meta description (collapsible)
  - **Status & Publishing:** Status dropdown, publication date, featured checkbox, comments enabled toggle
  - **Statistics:** Comments count (read-only, collapsible)
  - **Metadata:** Created/updated by, timestamps (collapsible)
  - **Inline Comments:** View and manage comments directly from blog post page
  - Save buttons at both top and bottom of form

- **Bulk Actions:**
  - Mark as published
  - Mark as draft
  - Mark as featured
  - Remove featured status

**Tips:**
- The slug is automatically generated from the title but can be edited
- Use the horizontal tag widget for easy tag selection
- Featured image preview shows immediately after upload
- Comments can be viewed inline on the blog post edit page

#### 2. Authors Management

**Location:** `/admin/api/author/`

**Features:**
- **List View:**
  - Author name
  - Blog posts count (clickable link to filtered posts)
  - Creation and update timestamps
  - Search by name

- **Edit/Create View:**
  - Author name field
  - Statistics section showing blog posts count (collapsible)
  - Metadata section (collapsible)

**Tips:**
- Click on the blog posts count to see all posts by that author
- Author names are displayed on blog posts

#### 3. Tags Management

**Location:** `/admin/api/tag/`

**Features:**
- **List View:**
  - Tag name and slug
  - Blog posts count (clickable link to filtered posts)
  - Creation timestamp
  - Search by name or slug

- **Edit/Create View:**
  - Tag name
  - Slug (auto-generated from name, but editable)
  - Statistics section showing blog posts count (collapsible)

**Tips:**
- Slugs are automatically generated from tag names
- Click on the blog posts count to see all posts with that tag
- Tags help organize and categorize content

#### 4. Comments Management

**Location:** `/admin/api/comment/`

**Features:**
- **List View:**
  - Commenter name and email
  - Blog post link (clickable)
  - Content preview (truncated to 100 characters)
  - Approval status badge (color-coded: green for approved, red for pending)
  - Creation timestamp
  - Date hierarchy for filtering by date
  - Advanced filtering (approval status, date, blog post)
  - Search (name, email, content, blog post title)

- **Edit View:**
  - Comment information (blog post, name, email, content)
  - Moderation section (approval checkbox)
  - Metadata (timestamps, collapsible)

- **Bulk Actions:**
  - Approve selected comments
  - Disapprove selected comments
  - Delete selected comments

**Tips:**
- Only approved comments appear on the website
- Use bulk actions to approve/disapprove multiple comments at once
- Click on blog post link to view the associated post
- Comments are automatically linked to their blog posts

### Admin Interface Features

#### Visual Enhancements

1. **Color-Coded Status Badges:**
   - Green: Published posts
   - Yellow: Draft posts
   - Gray: Archived posts
   - Blue: Featured posts

2. **Interactive Elements:**
   - Clickable counts that filter to related items
   - Image previews for featured images
   - Tag badges for easy visual identification
   - Status badges for quick recognition

3. **User-Friendly Organization:**
   - Collapsible sections for less-used fields
   - Fieldset descriptions for guidance
   - Logical grouping of related fields
   - Save buttons at top and bottom

#### Search and Filtering

- **Global Search:** Available in list views for quick finding
- **Advanced Filters:** Sidebar filters for common queries
- **Date Hierarchy:** Navigate by date ranges easily
- **Related Item Links:** Click counts to see filtered results

#### Bulk Operations

- Select multiple items using checkboxes
- Apply actions to multiple items at once
- Useful for:
  - Publishing multiple drafts
  - Approving multiple comments
  - Featuring multiple posts

### Admin Theme

The admin interface uses a **light theme by default** for better readability and a modern appearance. Users can still toggle to dark theme using the theme switcher if preferred.

### Best Practices

1. **Blog Posts:**
   - Always set a publication date for published posts
   - Use descriptive categories
   - Add relevant tags for better organization
   - Upload featured images for visual appeal
   - Fill in SEO meta fields for better search engine visibility

2. **Comments:**
   - Review comments regularly
   - Approve quality comments promptly
   - Use bulk actions for efficiency
   - Check comment content before approving

3. **Tags:**
   - Use consistent naming conventions
   - Avoid creating duplicate tags
   - Keep tag names concise and descriptive

4. **Authors:**
   - Create authors before creating blog posts
   - Use full names for better identification

### Admin URL Structure

```
/admin/                          - Admin dashboard
/admin/api/blogpost/             - Blog posts list
/admin/api/blogpost/add/         - Create new blog post
/admin/api/blogpost/{id}/change/ - Edit blog post
/admin/api/author/               - Authors list
/admin/api/tag/                  - Tags list
/admin/api/comment/              - Comments list
```

### Permissions

- **Staff Users:** Can access admin interface
- **Superusers:** Full access to all admin features
- **Regular Users:** Cannot access admin (API access only)

---

## Support

For issues or questions, please contact the development team.

