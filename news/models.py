"""
Django News Portal Models

This module contains the core data models for the news portal application,
including user management, article publishing, and subscription functionality.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from .constants import UserRoles, ArticleStatus, FileUpload


class Publisher(models.Model):
    """
    Represents a news publishing organization.
    
    Publishers can have multiple editors and journalists associated with them.
    Editors can moderate articles, while journalists can create content.
    """
    name = models.CharField(max_length=100)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="editor_of_publishers", blank=True
    )
    journalists = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="journalist_of_publishers", blank=True
    )

    def __str__(self):
        """Return the publisher's name as string representation."""
        return self.name


class CustomUser(AbstractUser):
    """
    Extended user model for the news portal application.
    
    Supports different user roles (reader, journalist, editor, publisher)
    with role-specific fields and functionality.
    """
    role = models.CharField(max_length=20, choices=UserRoles.CHOICES, default=UserRoles.READER)
    
    # Reader-only
    subscriptions_publishers = models.ManyToManyField(
        Publisher, related_name="subscribed_readers", blank=True
    )
    subscriptions_journalists = models.ManyToManyField(
        "self", symmetrical=False, related_name="subscribers", blank=True
    )

    # Shared fields
    profile_image = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    contact_number = models.CharField(max_length=32, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override save method to clear reader-only fields for non-reader roles.
        """
        super().save(*args, **kwargs)
        # If journalist, clear reader-only fields
        if self.role == UserRoles.JOURNALIST:
            self.subscriptions_publishers.clear()
            self.subscriptions_journalists.clear()

    def __str__(self):
        """Return the username as string representation."""
        return self.username

class Article(models.Model):
    """
    Represents a news article in the system.
    
    Articles go through a moderation process with pending, approved, and rejected states.
    Only approved articles are visible to the public.
    """
    # Status constants for backward compatibility
    STATUS_PENDING = ArticleStatus.PENDING
    STATUS_APPROVED = ArticleStatus.APPROVED
    STATUS_REJECTED = ArticleStatus.REJECTED
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to=FileUpload.ARTICLE_IMAGES, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ArticleStatus.CHOICES, default=ArticleStatus.PENDING)
    rejection_reason = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_articles"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Return article title with status information."""
        return f"{self.title} ({self.get_status_display()})"

    def get_absolute_url(self):
        """Return the canonical URL for this article."""
        from django.urls import reverse
        return reverse("article_detail", args=[str(self.pk)])

    @property
    def is_pending(self):
        """Check if article is in pending status."""
        return self.status == ArticleStatus.PENDING

    @property
    def is_approved(self):
        """Check if article is approved."""
        return self.status == ArticleStatus.APPROVED

    @property
    def is_rejected(self):
        """Check if article is rejected."""
        return self.status == ArticleStatus.REJECTED

    def approve(self, reviewer):
        """
        Approve the article and set reviewer information.
        
        Args:
            reviewer: The user who is approving the article
        """
        self.status = ArticleStatus.APPROVED
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()
        self.rejection_reason = ''
        self.save()

    def reject(self, reviewer, reason):
        """
        Reject the article with a reason and set reviewer information.
        
        Args:
            reviewer: The user who is rejecting the article
            reason: The reason for rejection
        """
        self.status = ArticleStatus.REJECTED
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()
        self.rejection_reason = reason
        self.save()

class Newsletter(models.Model):
    """
    Represents a newsletter created by journalists.
    
    Newsletters require approval from editors before being published.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    journalist = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="newsletters"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name="newsletters"
    )
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Return the newsletter title as string representation."""
        return self.title


class Subscription(models.Model):
    """
    Links a reader (CustomUser with role='reader') to a publisher.
    Editors / journalists are never stored here – they’re referenced
    via the Many‑to‑Many fields on Publisher.
    """
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="publisher_subscriptions",
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reader", "publisher")
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.reader.username} → {self.publisher.name}"
