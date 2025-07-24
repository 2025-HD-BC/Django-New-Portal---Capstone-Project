"""
Django News Portal Admin Configuration

This module contains the Django admin interface configuration for the news portal
application. It provides customized admin views for managing articles, publishers,
users, and newsletters with appropriate filtering and search capabilities.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, Publisher, CustomUser, Newsletter

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for Article management.
    
    Provides comprehensive article management with filtering by status, publisher,
    and creation date, plus search functionality across title, content, and author.
    """
    list_display = ("title", "author", "publisher", "status", "created_at")
    list_filter = ("status", "publisher", "created_at")
    search_fields = ("title", "content", "author__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Admin interface for Publisher management.
    
    Shows publisher information with counts of associated editors and journalists.
    """
    list_display = ("name", "editor_count", "journalist_count")
    search_fields = ("name",)

    def editor_count(self, obj):
        """Return the number of editors associated with this publisher."""
        return obj.editors.count()
    editor_count.short_description = "Editors"

    def journalist_count(self, obj):
        """Return the number of journalists associated with this publisher."""
        return obj.journalists.count()
    journalist_count.short_description = "Journalists"

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser management.
    
    Extends Django's default UserAdmin with role-specific fields and subscription
    management capabilities. Provides horizontal filter widgets for many-to-many
    relationships.
    """
    list_display = UserAdmin.list_display + ("role", "email")
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": (
                "role",
                "subscriptions_publishers",
                "subscriptions_journalists",
                "profile_image",
                "contact_number",
                "bio",
            )
        }),
    )
    filter_horizontal = ("subscriptions_publishers", "subscriptions_journalists")

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin interface for Newsletter management.
    
    Provides management of newsletters with filtering by approval status and
    creation date, plus search functionality across title, content, and journalist.
    """
    list_display = ("title", "journalist", "publisher", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("title", "content", "journalist__username")
    ordering = ("-created_at",)
