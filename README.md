# Django News Portal

A comprehensive news management system built with Django, featuring role-based access control, editorial workflows, and REST API integration.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](#license)

## 📋 Overview

The Django News Portal is a full-featured content management system designed for news organizations. It provides a complete editorial workflow with role-based permissions, article management, newsletter distribution, and comprehensive API access.

## ✨ Key Features

### 🏗️ **Core Functionality**
- **Multi-role User System**: Readers, journalists, editors, and publishers with distinct permissions
- **Editorial Workflow**: Complete article lifecycle from creation to publication
- **Publisher Management**: Organization-based content management
- **Newsletter System**: Create and distribute newsletters to subscribers
- **Subscription Management**: Reader engagement and notification system

### 🔧 **Technical Features**
- **REST API**: Comprehensive API with authentication and authorization
- **Admin Interface**: Customized Django admin with role-specific views
- **Docker Support**: Containerized deployment for easy setup
- **Database Flexibility**: Support for SQLite (development) and MySQL/MariaDB (production)
- **Security**: Environment-based configuration and secure secret management

### 📚 **Documentation & Quality**
- **Comprehensive Documentation**: Sphinx-generated documentation
- **Professional Docstrings**: Complete code documentation
- **Git Workflow**: Proper branching and version control
- **Testing Ready**: Structure prepared for comprehensive testing

## 👥 User Roles & Permissions

| Role | Capabilities | Access Level |
|------|-------------|--------------|
| 👤 **Reader** | View approved articles, subscribe to publishers/journalists | Public + Authenticated |
| ✍️ **Journalist** | Create articles and newsletters, manage own content | Content Creation |
| 📝 **Editor** | Review, approve/reject articles and newsletters | Content Moderation |
| 🏢 **Publisher** | Manage publishing organizations and editorial teams | Organization Management |

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)
- Git
- Docker (optional, for containerized deployment)

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/2025-HD-BC/Django-New-Portal---Capstone-Project.git
   cd Django_News_Portal
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-django-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Optional: Email configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # Optional: Social media integration
   TWITTER_API_KEY=your-twitter-api-key
   TWITTER_API_SECRET=your-twitter-api-secret
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - API documentation: http://127.0.0.1:8000/api/

### Option 2: Docker Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/2025-HD-BC/Django-New-Portal---Capstone-Project.git
   cd Django_News_Portal
   ```

2. **Build Docker image**
   ```bash
   docker build -t django-news-portal .
   ```

3. **Run container**
   ```bash
   docker run -p 8000:8000 django-news-portal
   ```

4. **Access the application**
   - Main application: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/

### Option 3: Using Makefile (if available)

```bash
# View available commands
make help

# Set up development environment
make dev-setup

# Run with Docker
make docker-build
make docker-run
```

## 🏗️ Project Structure

```
Django_News_Portal/
├── 📁 news/                    # Main Django application
│   ├── 📄 models.py           # Data models with comprehensive docstrings
│   ├── 📄 views.py            # View functions and business logic
│   ├── 📄 forms.py            # Django forms for user input
│   ├── 📄 admin.py            # Custom admin interface
│   ├── 📄 constants.py        # Application constants and choices
│   ├── 📄 permissions.py      # Custom permission classes
│   ├── 📄 signals.py          # Django signals for automation
│   ├── 📁 api/                # REST API implementation
│   ├── 📁 management/         # Custom Django commands
│   ├── 📁 migrations/         # Database migrations
│   ├── 📁 static/             # Static files (CSS, JS, images)
│   └── 📁 templates/          # HTML templates
├── 📁 news_app/               # Django project configuration
│   ├── 📄 settings.py         # Main settings
│   ├── 📄 sqlite_settings.py  # SQLite-specific settings
│   ├── 📄 urls.py             # URL routing
│   └── 📄 wsgi.py             # WSGI configuration
├── 📁 docs/                   # Sphinx documentation
│   ├── 📄 conf.py             # Sphinx configuration
│   ├── 📄 index.rst           # Documentation index
│   └── 📁 _build/html/        # Generated HTML documentation
├── 📁 media/                  # User uploaded files
├── 📁 static/                 # Collected static files
├── 📄 requirements.txt        # Python dependencies
├── 📄 Dockerfile             # Docker configuration
├── 📄 .dockerignore          # Docker ignore rules
├── 📄 .gitignore             # Git ignore rules
├── 📄 manage.py              # Django management script
├── 📄 create_demo_data.py    # Demo data generation script
└── 📄 README.md              # This file
```

## 🔌 API Documentation

The Django News Portal provides a comprehensive REST API for external integrations and mobile applications.

### Authentication

The API supports multiple authentication methods:
- Session Authentication (for web applications)
- Token Authentication (for mobile/external apps)

### Core Endpoints

| Endpoint | Method | Description | Authentication |
|----------|---------|-------------|----------------|
| `/api/` | GET | API root and overview | None |
| `/api/articles/` | GET | List approved articles | None |
| `/api/articles/` | POST | Create new article | Required (Journalist+) |
| `/api/articles/{id}/` | GET | Article details | None |
| `/api/articles/{id}/` | PUT/PATCH | Update article | Required (Author/Editor) |
| `/api/articles/{id}/` | DELETE | Delete article | Required (Author/Editor) |
| `/api/publishers/` | GET | List publishers | None |
| `/api/publishers/{id}/` | GET | Publisher details | None |
| `/api/newsletters/` | GET | List newsletters | None |
| `/api/newsletters/` | POST | Create newsletter | Required (Journalist+) |

### Example API Usage

```bash
# Get all approved articles
curl -X GET http://localhost:8000/api/articles/

# Create a new article (requires authentication)
curl -X POST http://localhost:8000/api/articles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-api-token" \
  -d '{
    "title": "Breaking News Title",
    "content": "Article content here...",
    "publisher": 1
  }'

# Get publisher information
curl -X GET http://localhost:8000/api/publishers/1/
```

## 🧪 Testing

The project includes a comprehensive testing structure:

```bash
# Run all tests
python manage.py test

# Run tests with coverage (if coverage is installed)
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML coverage report

# Run specific test modules
python manage.py test news.tests
python manage.py test news.api.tests
```

## 📚 Documentation

### Sphinx Documentation

Comprehensive documentation is generated using Sphinx:

1. **Build documentation**
   ```bash
   cd docs
   make html
   ```

2. **View documentation**
   Open `docs/_build/html/index.html` in your browser

### API Documentation

API documentation is available at `/api/` when running the development server.

## 🔒 Security Considerations

### Environment Variables

**⚠️ IMPORTANT**: Never commit sensitive information to version control.

Required environment variables for production:

```env
# Core Django settings
SECRET_KEY=your-unique-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database configuration (example for MySQL)
DATABASE_URL=mysql://username:password@localhost/database_name

# Email configuration
EMAIL_HOST=smtp.yourdomain.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True

# Optional: Social media integration
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-token-secret
```

### Production Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Set up proper database (PostgreSQL/MySQL)
- [ ] Configure static file serving
- [ ] Set up SSL/HTTPS
- [ ] Configure proper logging
- [ ] Set up backup systems

## 🔧 Development

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** with proper testing
5. **Commit with descriptive messages**
   ```bash
   git commit -m "Add: New feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Code Standards

- Follow PEP 8 Python style guidelines
- Write comprehensive docstrings for all functions and classes
- Include unit tests for new functionality
- Update documentation for any API changes
- Use meaningful variable and function names

### Git Workflow

This project follows a feature branch workflow:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Individual feature branches
- `hotfix/*` - Critical bug fixes

## 📊 Features in Detail

### Editorial Workflow

```mermaid
graph TD
    A[Journalist Creates Article] --> B[Article Status: PENDING]
    B --> C{Editor Review}
    C -->|Approve| D[Article Status: APPROVED]
    C -->|Reject| E[Article Status: REJECTED]
    D --> F[Notify Subscribers]
    D --> G[Publish to Website]
    E --> H[Notify Author]
```

### User Management

- **Custom User Model** with role-based permissions
- **Group-based Authorization** for different user types
- **Profile Management** with additional user information
- **Subscription System** for reader engagement

### Content Management

- **Rich Text Editor** for article creation
- **Image Upload** and management
- **Category System** for content organization
- **Tag Support** for content discovery
- **Search Functionality** across articles

## 🚀 Deployment Options

### Traditional Hosting

1. **Prepare production settings**
2. **Set up database** (PostgreSQL recommended)
3. **Configure web server** (Nginx + Gunicorn)
4. **Set up SSL certificate**
5. **Configure static file serving**

### Docker Production

```dockerfile
# Production Dockerfile example
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "news_app.wsgi:application"]
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute

- 🐛 **Bug Reports**: Report bugs using GitHub Issues
- 💡 **Feature Requests**: Suggest new features
- 📝 **Documentation**: Improve documentation
- 🧪 **Testing**: Add test coverage
- 🔧 **Code**: Submit pull requests

## 📄 License

This project is created as an educational capstone project demonstrating advanced Django development skills, including:

- Full-stack web development
- RESTful API design
- Database modeling and relationships
- User authentication and authorization
- Docker containerization
- Professional documentation practices
- Git version control workflows

## 🙏 Acknowledgments

- Django Software Foundation for the excellent framework
- Python community for comprehensive libraries
- Bootstrap team for responsive UI components
- Docker team for containerization technology

## 📞 Support

For questions about this educational project:

1. **Check the documentation** in the `docs/` directory
2. **Review the code comments** and docstrings
3. **Examine the test files** for usage examples
4. **Create an issue** on GitHub for bugs or questions

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

Built with ❤️ using Django and Python

[🔝 Back to top](#django-news-portal)

</div>
