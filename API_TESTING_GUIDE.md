# News Portal API Testing Guide

## Overview
Your Django REST Framework API is fully configured and ready for testing. The API provides endpoints for third-party clients to retrieve articles, publishers, users, and newsletters based on subscriptions.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Available Endpoints

### 1. Articles API
- **GET /api/articles/** - List all approved articles
- **GET /api/articles/{id}/** - Get specific article details
- **POST /api/articles/{id}/approve/** - Approve article (editors only)

### 2. Publishers API
- **GET /api/publishers/** - List all publishers
- **GET /api/publishers/{id}/** - Get specific publisher details

### 3. Users API
- **GET /api/users/** - List users (authenticated access)
- **GET /api/users/{id}/** - Get specific user details

### 4. Newsletters API
- **GET /api/newsletters/** - List newsletters
- **GET /api/newsletters/{id}/** - Get specific newsletter details

### 5. Subscription Feed API
- **GET /api/subscriptions/feed/** - Get articles for subscribed publishers/journalists

## Testing with Browser (GET requests)
Visit these URLs directly in your browser:
1. http://127.0.0.1:8000/api/articles/
2. http://127.0.0.1:8000/api/publishers/
3. http://127.0.0.1:8000/api/newsletters/

## Testing with Postman

### Authentication
For protected endpoints, include authentication headers:
```
Authorization: Token {your-api-token}
```
Or use session authentication if logged in via browser.

### Example Requests

#### 1. Get All Articles
```
GET http://127.0.0.1:8000/api/articles/
```

#### 2. Get Specific Article
```
GET http://127.0.0.1:8000/api/articles/1/
```

#### 3. Approve Article (Editors Only)
```
POST http://127.0.0.1:8000/api/articles/1/approve/
Authorization: Token {editor-token}
```

#### 4. Get Subscription Feed
```
GET http://127.0.0.1:8000/api/subscriptions/feed/
Authorization: Token {user-token}
```

## Response Format
All responses are in JSON format:

### Article Response Example:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Breaking News",
      "content": "Article content...",
      "image": "/media/articles/image.jpg",
      "author": {
        "id": 2,
        "username": "journalist1",
        "email": "journalist@example.com",
        "role": "journalist"
      },
      "publisher": {
        "id": 1,
        "name": "News Corp"
      },
      "status": "approved",
      "created_at": "2025-07-22T10:00:00Z",
      "reviewed_at": "2025-07-22T11:00:00Z",
      "rejection_reason": null
    }
  ]
}
```

## API Features
✅ **Serialization**: JSON/XML format support
✅ **Authentication**: Token and Session authentication
✅ **Permissions**: Role-based access control
✅ **Filtering**: Subscription-based article filtering
✅ **CRUD Operations**: Full Create, Read, Update, Delete support
✅ **Approval Workflow**: Editor approval system
✅ **Error Handling**: Proper HTTP status codes

## Unit Tests
Your API includes comprehensive unit tests in `news/api/tests.py`:
- Article list/detail tests
- Approval endpoint tests  
- Subscription feed tests
- Permission-based access tests

## Next Steps
1. Test endpoints using browser or Postman
2. Verify authentication works correctly
3. Test subscription-based filtering
4. Validate permission controls
5. Document any issues found

