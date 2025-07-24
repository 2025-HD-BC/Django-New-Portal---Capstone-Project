# news/constants.py
"""
Constants used throughout the news application.
"""

# User role constants
class UserRoles:
    READER = "reader"
    EDITOR = "editor" 
    JOURNALIST = "journalist"
    PUBLISHER = "publisher"
    
    CHOICES = [
        (READER, "Reader"),
        (EDITOR, "Editor"),
        (JOURNALIST, "Journalist"),
        (PUBLISHER, "Publisher"),
    ]
    
    @classmethod
    def get_all_roles(cls):
        """Return all available role values."""
        return [cls.READER, cls.EDITOR, cls.JOURNALIST, cls.PUBLISHER]


# Article status constants  
class ArticleStatus:
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
    CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'), 
        (REJECTED, 'Rejected'),
    ]


# Permission constants
class Permissions:
    """Common permission checks and group names."""
    
    # Group names (should match UserRoles)
    READER_GROUP = UserRoles.READER
    EDITOR_GROUP = UserRoles.EDITOR
    JOURNALIST_GROUP = UserRoles.JOURNALIST
    PUBLISHER_GROUP = UserRoles.PUBLISHER
    
    # Permission codenames
    VIEW_ARTICLE = 'view_article'
    ADD_ARTICLE = 'add_article'
    CHANGE_ARTICLE = 'change_article'
    DELETE_ARTICLE = 'delete_article'
    
    VIEW_NEWSLETTER = 'view_newsletter'
    ADD_NEWSLETTER = 'add_newsletter'
    CHANGE_NEWSLETTER = 'change_newsletter'
    DELETE_NEWSLETTER = 'delete_newsletter'


# API endpoint constants
class APIEndpoints:
    """API URL patterns and names."""
    ARTICLES = 'api/articles/'
    PUBLISHERS = 'api/publishers/'
    USERS = 'api/users/'
    NEWSLETTERS = 'api/newsletters/'
    SUBSCRIPTION_FEED = 'api/subscriptions/feed/'
    ARTICLE_APPROVE = 'api/articles/{id}/approve/'


# Email and notification constants
class NotificationSettings:
    DEFAULT_FROM_EMAIL = 'noreply@newsportal.com'
    EMAIL_TIMEOUT = 30  # seconds
    MAX_EMAIL_RECIPIENTS = 100
    
    # Email subject templates
    ARTICLE_APPROVED_SUBJECT = "New Article: {title}"
    NEWSLETTER_SUBJECT = "Newsletter: {title}"
    PASSWORD_RESET_SUBJECT = "Password Reset - News Portal"


# File upload constants
class FileUpload:
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_FORMATS = ['JPEG', 'JPG', 'PNG', 'GIF']
    
    # Upload paths
    ARTICLE_IMAGES = 'articles/'
    PROFILE_PICS = 'profile_pics/'
    
    # Image dimensions
    PROFILE_IMAGE_SIZE = (300, 300)
    ARTICLE_IMAGE_MAX_SIZE = (1200, 800)


# Pagination constants
class Pagination:
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Per-model page sizes
    ARTICLES_PER_PAGE = 12
    NEWSLETTERS_PER_PAGE = 10
    USERS_PER_PAGE = 25


# Cache keys and timeouts
class CacheSettings:
    ARTICLE_LIST_TIMEOUT = 300  # 5 minutes
    PUBLISHER_LIST_TIMEOUT = 600  # 10 minutes
    USER_DASHBOARD_TIMEOUT = 180  # 3 minutes
    
    # Cache key templates
    ARTICLE_LIST_KEY = 'articles_approved'
    PUBLISHER_ARTICLES_KEY = 'publisher_{id}_articles'
    USER_DASHBOARD_KEY = 'user_{id}_dashboard'
