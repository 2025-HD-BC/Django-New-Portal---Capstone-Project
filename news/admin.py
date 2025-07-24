from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, Publisher, CustomUser, Newsletter

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publisher", "status", "created_at")
    list_filter = ("status", "publisher", "created_at")
    search_fields = ("title", "content", "author__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "editor_count", "journalist_count")
    search_fields = ("name",)

    def editor_count(self, obj):
        return obj.editors.count()
    editor_count.short_description = "Editors"

    def journalist_count(self, obj):
        return obj.journalists.count()
    journalist_count.short_description = "Journalists"

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
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
    list_display = ("title", "journalist", "publisher", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("title", "content", "journalist__username")
    ordering = ("-created_at",)
