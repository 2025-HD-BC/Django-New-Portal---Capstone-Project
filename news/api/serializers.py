# news/api/serializers.py
from rest_framework import serializers

from news.models import (
    Article,
    Publisher,
    CustomUser,
    Newsletter,      
)

# ───────────────────────────────────────────────────────────────────
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Publisher
        fields = ["id", "name"]


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CustomUser
        fields = ["id", "username", "email", "role"]


class ArticleSerializer(serializers.ModelSerializer):
    author    = CustomUserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model  = Article
        fields = [
            "id",
            "title",
            "content",
            "image",
            "author",
            "publisher",
            "status",
            "created_at",
            "reviewed_at",
            "rejection_reason",
        ]
        read_only_fields = [
            "id",
            "author",
            "status",
            "created_at",
            "reviewed_at",
            "rejection_reason",
        ]

# ───────────────────────────────────────────────────────────────────
# NEW  ▸  Newsletter serializer
# ───────────────────────────────────────────────────────────────────
class NewsletterSerializer(serializers.ModelSerializer):
    journalist = CustomUserSerializer(read_only=True)
    publisher  = PublisherSerializer(read_only=True)

    class Meta:
        model  = Newsletter
        fields = [
            "id",
            "title",
            "content",
            "journalist",
            "publisher",
            "approved",
            "created_at",
        ]
        read_only_fields = ["id", "journalist", "approved", "created_at"]
