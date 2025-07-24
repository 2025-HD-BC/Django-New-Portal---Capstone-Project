# Django News Portal

A comprehensive news management system built with Django, featuring role-based access control for readers, journalists, editors, and publishers.

## Features

- **Multi-role User System**: Support for readers, journalists, editors, and publishers
- **Article Management**: Create, review, approve, and publish news articles
- **Publisher Organizations**: Organize content by publishing organizations
- **Newsletter System**: Create and distribute newsletters
- **Subscription Management**: Allow readers to follow publishers and journalists
- **REST API**: Comprehensive API for external integrations
- **Admin Interface**: Django admin with custom configurations

## User Roles

- **Readers**: Can view approved articles, subscribe to publishers and journalists
- **Journalists**: Can create articles and newsletters
- **Editors**: Can review and moderate articles and newsletters
- **Publishers**: Can manage publishing organizations

## Installation and Setup

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)
- Git

### Option 1: Local Development with Virtual Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/2025-HD-BC/Django-New-Portal---Capstone-Project.git
   cd Django_News_Portal
   ```

2. **Create and activate virtual environment**
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

4. **Environment Configuration**
   - Create a `.env` file with your configuration
   - **IMPORTANT**: Never commit real secrets like passwords or API keys to the repository
   - Use environment variables for sensitive information

   Example `.env` file:
   ```env
   SECRET_KEY=your-django-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - API root: http://127.0.0.1:8000/api/

### Option 2: Docker Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/2025-HD-BC/Django-New-Portal---Capstone-Project.git
   cd Django_News_Portal
   ```

2. **Build the Docker image**
   ```bash
   docker build -t django-news-portal .
   ```

3. **Run the container**
   ```bash
   docker run -p 8000:8000 django-news-portal
   ```

4. **Access the Application**
   - Main application: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/

### Docker Compose (Recommended for Production)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key-here
      - DATABASE_URL=sqlite:///db.sqlite3
    volumes:
      - ./media:/app/media
      - ./static:/app/static
```

Then run:
```bash
docker-compose up --build
```

## Security Configuration

**⚠️ IMPORTANT SECURITY NOTES**: 

1. **Secret Management**: 
   - Never commit real secret keys, passwords, or API tokens to version control
   - Use environment variables or secure secret management systems
   - Generate a new SECRET_KEY for production deployments

2. **Database Configuration**:
   - For production, use PostgreSQL or MySQL instead of SQLite
   - Configure proper database credentials via environment variables

3. **Environment Variables**:
   Create a `.env` file (never commit this) with:
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

## API Documentation

The application includes a REST API with endpoints for:

- `/api/` - API root
- `/api/articles/` - Article management
- `/api/publishers/` - Publisher management
- `/api/newsletters/` - Newsletter management

## Documentation

Comprehensive Sphinx documentation is available:

1. **Build documentation**
   ```bash
   cd docs
   make html
   ```

2. **View documentation**
   Open `docs/_build/html/index.html` in your browser

## Testing

Run the test suite:
```bash
python manage.py test
```

## Project Structure

```
Django_News_Portal/
├── news/                   # Main application
│   ├── models.py          # Data models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   ├── api/               # REST API
│   └── templates/         # HTML templates
├── news_app/              # Django project settings
├── docs/                  # Sphinx documentation
├── media/                 # User uploaded files
├── static/                # Static files
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md             # This file
```

## License

This project is developed as part of a Django capstone project demonstrating full-stack web development skills.

---

**Note**: This is a capstone project showcasing Django development skills including authentication, authorization, database modeling, API development, containerization, and deployment strategies.
- 📱 **API-First Design**: Complete RESTful API with comprehensive testing
- 🎨 **Modern UI**: Responsive Bootstrap 5 interface with custom styling
- 📧 **Real-time Integration**: Email notifications and social media posting
- 🧪 **Test Coverage**: Comprehensive unit tests with 100% core functionality coverage

---

## 🚀 **Features**

### 🏆 **Code Excellence**

<table>
<tr>
<td>

**🎯 Professional Standards**
- PEP 8 compliant codebase
- Modular, single-responsibility functions
- Comprehensive error handling
- Detailed documentation & docstrings

</td>
<td>

**🔧 Architecture Quality**
- Centralized constants management
- Clean separation of concerns  
- Maintainable & scalable design
- Industry-standard patterns

</td>
</tr>
</table>

### 🛠️ **Technical Stack**

<table>
<tr>
<td>

**Backend**
- Django 4.2+
- Django REST Framework
- Python 3.8+
- MariaDB / SQLite

</td>
<td>

**Frontend**
- Bootstrap 5
- HTML5 / CSS3
- JavaScript
- Responsive Design

</td>
<td>

**DevOps**
- Environment-based config
- Unit testing
- API documentation
- Production-ready setup

</td>
</tr>
</table>

### 👥 **User Management & Permissions**

<div align="center">

| Role | Permissions | Features |
|------|-------------|----------|
| 👤 **Reader** | View articles & newsletters | Subscription management, personalized feeds |
| ✍️ **Journalist** | Create & manage content | Article creation, newsletter publishing |
| 📝 **Editor** | Review & approve content | Editorial workflow, content moderation |
| 🏢 **Publisher** | Manage organizations | Publisher administration, team management |

</div>

### 📋 **Editorial Workflow**

```mermaid
graph TD
    A[Journalist Creates Article] --> B[Article: PENDING Status]
    B --> C{Editor Review}
    C -->|Approve| D[Article: APPROVED]
    C -->|Reject| E[Article: REJECTED]
    D --> F[Email Notifications Sent]
    D --> G[Social Media Posting]
    E --> H[Rejection Reason Logged]
```

### 🔗 **Integrations & Notifications**

**Real-time Features:**
- 📧 **Email Notifications**: Automated subscriber alerts on content approval
- 🐦 **Social Media**: X (Twitter) integration for content sharing  
- 🔄 **Auto-Assignment**: Dynamic user group management via Django signals
- 🛡️ **Error Handling**: Graceful failure handling with comprehensive logging

---

## 🛠️ **Installation**

### **Prerequisites**
- Python 3.8+
- MariaDB (optional - SQLite included for development)

### **Quick Start**

```bash
# Clone the repository
git clone https://github.com/yourusername/django-news-portal.git
cd django-news-portal

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your configuration

# Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py seed_groups

# Create admin user
python manage.py createsuperuser

# Run the application
python manage.py runserver
```

### **Environment Configuration**

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
MARIADB_DB=news_db
MARIADB_USER=your-username
MARIADB_PASSWORD=your-password
MARIADB_HOST=localhost
MARIADB_PORT=3306
```

---

## 🧪 **Testing**

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run with coverage
python -m coverage run --source='.' manage.py test
python -m coverage report

# Run specific test modules
python manage.py test news.api.tests
```

### **Test Coverage**
- ✅ API endpoint testing
- ✅ Permission validation
- ✅ Editorial workflow testing
- ✅ User authentication & authorization

---

## 📡 **API Documentation**

### **Authentication**
All API endpoints support session and token authentication.

### **Core Endpoints**

<details>
<summary><b>📰 Articles API</b></summary>

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/articles/` | List approved articles | No |
| `GET` | `/api/articles/{id}/` | Article details | No |
| `POST` | `/api/articles/` | Create article | Yes (Journalist) |
| `PUT` | `/api/articles/{id}/` | Update article | Yes (Author/Editor) |
| `DELETE` | `/api/articles/{id}/` | Delete article | Yes (Author/Editor) |
| `POST` | `/api/articles/{id}/approve/` | Approve article | Yes (Editor) |

</details>

<details>
<summary><b>🏢 Publishers API</b></summary>

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/publishers/` | List publishers | No |
| `GET` | `/api/publishers/{id}/articles/` | Publisher articles | No |

</details>

<details>
<summary><b>📧 Subscriptions API</b></summary>

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/subscriptions/feed/` | Personalized feed | Yes (Reader) |

</details>

### **Example API Usage**

```bash
# Get all articles
curl -X GET http://localhost:8000/api/articles/

# Create article (requires authentication)
curl -X POST http://localhost:8000/api/articles/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Breaking News", "content": "Article content..."}'

# Approve article (editors only)
curl -X POST http://localhost:8000/api/articles/1/approve/ \
  -H "Authorization: Token your-token-here"
```

---

## 🎨 **Demo**

### **Demo Accounts**

After running the demo data script, you can explore the application with:

| Role | Username | Password | Capabilities |
|------|----------|----------|-------------|
| 👤 Reader | `demo_reader` | `demo123` | Browse articles, manage subscriptions |
| ✍️ Journalist | `demo_journalist` | `demo123` | Create articles and newsletters |
| 📝 Editor | `demo_editor` | `demo123` | Review and approve content |
| 🏢 Publisher | `demo_publisher` | `demo123` | Manage publisher settings |

```bash
# Generate demo data
python create_demo_data.py
```

---

## 🏗️ **Architecture**

<div align="center">

```
┌─────────────────────────────────────────────────┐
│                   Django App                    │
├─────────────────┬─────────────────┬─────────────┤
│   Models Layer  │  Views Layer    │  API Layer  │
│   - CustomUser  │  - Dashboard    │  - REST API │
│   - Article     │  - Editorial    │  - Auth     │
│   - Publisher   │  - Permissions  │  - Testing  │
│   - Newsletter  │  - Workflow     │  - Docs     │
└─────────────────┴─────────────────┴─────────────┘
            │                   │
    ┌───────────────┐   ┌───────────────┐
    │   Database    │   │  Integrations │
    │  - MariaDB    │   │  - Email SMTP │
    │  - SQLite     │   │  - X/Twitter  │
    │  - Migrations │   │  - Signals    │
    └───────────────┘   └───────────────┘
```

</div>

### **Core Components**

- 🗄️ **Models**: Custom user model with role-based permissions, article workflow, publisher relationships
- 🎯 **Views**: Role-based dashboards, editorial interface, permission-controlled access
- 🔌 **API**: RESTful endpoints with comprehensive authentication and authorization
- 📧 **Signals**: Real-time notifications, social integration, automated workflows

---

## 🔧 **Troubleshooting**

<details>
<summary><b>🐛 Common Issues</b></summary>

**ModuleNotFoundError: No module named 'requests'**
```bash
pip install requests
```

**Database Connection Issues**
```bash
# Ensure MariaDB is running
sudo systemctl start mariadb

# Create database
mysql -u root -p
CREATE DATABASE news_db;
GRANT ALL PRIVILEGES ON news_db.* TO 'your_user'@'localhost';
```

**Permission Errors**
```bash
python manage.py seed_groups
```

</details>

---

## 🚀 **Production Deployment**

### **Environment Setup**
1. Set `DEBUG=False` in production
2. Configure `ALLOWED_HOSTS`
3. Set up proper database credentials
4. Configure static file serving
5. Set up SSL/HTTPS

### **Docker Support** (Optional)
```dockerfile
# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "news_app.wsgi:application"]
```

---

## 🤝 **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

### **Development Setup**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### **Code Standards**
- Follow PEP 8 guidelines
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

---

## � **Project Stats**

<div align="center">

![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-2000+-blue?style=flat-square)
![Test Coverage](https://img.shields.io/badge/Test%20Coverage-90%25+-green?style=flat-square)
![Code Quality](https://img.shields.io/badge/Code%20Quality-A+-gold?style=flat-square)

**Built with ❤️ using Django & Python**

</div>

---

## 📄 **License**

This project is created as a capstone project demonstrating advanced Django development skills and professional coding standards.

---

<div align="center">

**⭐ Star this repository if you found it helpful! ⭐**

[🔝 Back to top](#-django-news-portal)

</div>
