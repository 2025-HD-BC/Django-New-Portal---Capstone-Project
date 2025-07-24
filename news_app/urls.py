# news_app/urls.py
"""
Root URL configuration for the project.

• Admin interface     -> /admin/
• Front‑end pages     -> news.urls
• Built‑in auth views -> /accounts/
• REST API            -> /api/  (provided by news.api.urls)
"""

from pathlib import Path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from news.views import RoleBasedLoginView, MyLogoutView

urlpatterns = [
    # Favicon
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon-32.svg')),

    # Main application (HTML pages)
    path("", include("news.urls")),

    # Custom authentication views (login/logout)
    path("accounts/login/", RoleBasedLoginView.as_view(), name="login"),
    path("accounts/logout/", MyLogoutView.as_view(), name="logout"),

    # Built-in auth views (password reset, etc.) - custom config without login/logout
    path("accounts/", include("news_app.custom_auth_urls")),

    # Django admin (moved to end to avoid conflicts)
    path("admin/", admin.site.urls),

    # REST API (DRF)
    path("api/", include("news.api.urls")),
]

# Serve user‑uploaded media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler403 = "news.views.custom_403"
handler404 = "news.views.custom_404"
handler500 = "news.views.custom_500"
