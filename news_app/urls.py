"""
Django News Portal - Root URL Configuration

This module defines the main URL routing for the Django News Portal project.
It configures routing for:
• Admin interface     -> /admin/
• Front-end pages     -> news.urls  
• Built-in auth views -> /accounts/
• REST API            -> /api/ (provided by news.api.urls)
"""

from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from news.views import RoleBasedLoginView, MyLogoutView

urlpatterns = [
    # SITE FAVICON
    path(
        'favicon.ico', 
        RedirectView.as_view(url=settings.STATIC_URL + 'favicon-32.svg')
    ),

    # MAIN APPLICATION ROUTES (HTML pages)
    path("", include("news.urls")),

    # CUSTOM AUTHENTICATION VIEWS (login/logout)
    path("accounts/login/", RoleBasedLoginView.as_view(), name="login"),
    path("accounts/logout/", MyLogoutView.as_view(), name="logout"),

    # BUILT-IN AUTH VIEWS (password reset, etc.)
    path("accounts/", include("news_app.custom_auth_urls")),

    # DJANGO ADMIN INTERFACE
    path("admin/", admin.site.urls),

    # REST API ENDPOINTS (Django REST Framework)
    path("api/", include("news.api.urls")),
]

# STATIC & MEDIA FILE SERVING (Development only)
# Serve user-uploaded media files and static files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

# CUSTOM ERROR HANDLERS
handler403 = "news.views.custom_403"
handler404 = "news.views.custom_404"
handler500 = "news.views.custom_500"
