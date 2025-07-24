import os
from pathlib import Path

from decouple import config
from django.contrib.messages import constants as msg

BASE_DIR = Path(__file__).resolve().parent.parent


# 🔐 SECURITY
SECRET_KEY = config("SECRET_KEY", default="insecure-secret-key")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,kubernetes.docker.internal",
    cast=lambda v: [s.strip() for s in v.split(",")]
)


# 📦 INSTALLED APPS
INSTALLED_APPS = [
    # Django contrib apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",

    # Your apps
    "news",
]


# 🧩 MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# 🔗 URL CONF
ROOT_URLCONF = "news_app.urls"


# 🧠 TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",          # global templates & auth overrides
        ],
        "APP_DIRS": True,                   # also looks in news/templates/
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# 🗄️ WSGI
WSGI_APPLICATION = "news_app.wsgi.application"


# 🗄️ DATABASE (SQLite for development, MariaDB for production)
# Check if MariaDB credentials are provided, otherwise use SQLite
if config("MARIADB_DB", default=""):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": config("MARIADB_DB"),
            "USER": config("MARIADB_USER"),
            "PASSWORD": config("MARIADB_PASSWORD"),
            "HOST": config("MARIADB_HOST", default="localhost"),
            "PORT": config("MARIADB_PORT", default="3306"),
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # SQLite fallback for development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# 👤 CUSTOM USER
AUTH_USER_MODEL = "news.CustomUser"


# 🔒 PASSWORD VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        )
    },
]


# 🌍 INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# 📁 STATIC & MEDIA
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",   # for your CSS/JS/images during development
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstatic target (production)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# 🧠 MESSAGE TAGS (for styling in your templates)
MESSAGE_TAGS = {
    msg.DEBUG: "debug",
    msg.INFO: "info",
    msg.SUCCESS: "success",
    msg.WARNING: "warning",
    msg.ERROR: "danger",
}


# 🔮 DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# 🧰 DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}


# 📧 EMAIL SETTINGS
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=config("EMAIL_HOST_USER", default="noreply@newsportal.com"))
SERVER_EMAIL = config("SERVER_EMAIL", default=config("EMAIL_HOST_USER", default="noreply@newsportal.com"))

# Password reset settings
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour in seconds

# 🌐 DOMAIN SETTINGS
DOMAIN = config("DOMAIN", default="localhost:8000")

# 🐦 X (TWITTER) API SETTINGS
# OAuth 1.0a credentials for posting tweets
X_API_KEY = config("X_API_KEY", default="")
X_API_SECRET = config("X_API_SECRET", default="")
X_ACCESS_TOKEN = config("X_ACCESS_TOKEN", default="")
X_ACCESS_TOKEN_SECRET = config("X_ACCESS_TOKEN_SECRET", default="")
X_BEARER_TOKEN = config("X_BEARER_TOKEN", default="")

# OAuth 2.0 credentials (if needed for other operations)
X_CLIENT_ID = config("X_CLIENT_ID", default="")
X_CLIENT_SECRET = config("X_CLIENT_SECRET", default="")

# Twitter/X OAuth callback URL
X_REDIRECT_URI = config("X_REDIRECT_URI", default="http://craftle.co.za/twitter/callback/")

# Base URL for your application
BASE_URL = config("BASE_URL", default="http://127.0.0.1:8000")

# Authentication URLs
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'