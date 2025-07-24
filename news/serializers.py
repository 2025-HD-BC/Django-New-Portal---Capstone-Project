from rest_framework import serializers
from .models import Article, Publisher, CustomUser

class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for Publisher objects."""
    class Meta:
        model = Publisher
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article objects.
    Shows author username and full publisher details.
    """
    author = serializers.StringRelatedField()
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser objects (limited fields)."""
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "role")
        
