# Blog API Documentation

This directory contains the API documentation for the Blog application.

## Documentation Files

- **[API.md](./API.md)** - Complete API reference documentation with all endpoints, request/response examples, data models, and Django Admin interface guide.

## Quick Start

### Base URL
```
http://your-domain.com/api/
```

### Main Endpoints

1. **Health Check** - `GET /api/health/`
2. **List Blog Posts** - `GET /api/posts/`
3. **Get Blog Post** - `GET /api/posts/{id}/`
4. **Create Comment** - `POST /api/posts/{post_id}/comments/`
5. **List Comments** - `GET /api/posts/{post_id}/comments/list/`

### Example: Create a Comment

```bash
curl -X POST http://your-domain.com/api/posts/{post_id}/comments/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "content": "Great article!"
  }'
```

## Features

- ✅ RESTful API design
- ✅ Pagination support
- ✅ Search and filtering
- ✅ Comment system with moderation
- ✅ Tag management
- ✅ Image upload support
- ✅ SEO-friendly metadata
- ✅ User-friendly Django Admin interface
- ✅ Light theme by default

## For More Details

See [API.md](./API.md) for complete documentation including:
- Detailed endpoint descriptions
- Request/response examples
- Data models
- Error handling
- Code examples in multiple languages
- Django Admin interface guide
- Admin features and best practices

