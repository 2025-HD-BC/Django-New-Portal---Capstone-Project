#!/usr/bin/env python
"""
Demo script for the News Application
This script creates sample data to demonstrate the application functionality.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_app.settings')
django.setup()

from django.contrib.auth.models import Group
from news.models import CustomUser, Publisher, Article, Newsletter


def create_demo_data():
    """Create sample data for demonstration purposes."""
    print("Creating demo data...")
    
    # Create users with different roles
    try:
        # Reader
        reader = CustomUser.objects.create_user(
            username="demo_reader",
            email="reader@example.com",
            password="demo123",
            role="reader"
        )
        print(f"Created reader: {reader.username}")
        
        # Journalist
        journalist = CustomUser.objects.create_user(
            username="demo_journalist",
            email="journalist@example.com",
            password="demo123",
            role="journalist"
        )
        print(f"Created journalist: {journalist.username}")
        
        # Editor
        editor = CustomUser.objects.create_user(
            username="demo_editor",
            email="editor@example.com",
            password="demo123",
            role="editor"
        )
        print(f"Created editor: {editor.username}")
        
        # Publisher
        publisher_user = CustomUser.objects.create_user(
            username="demo_publisher",
            email="publisher@example.com",
            password="demo123",
            role="publisher"
        )
        print(f"Created publisher user: {publisher_user.username}")
        
        # Create publisher organization
        publisher_org = Publisher.objects.create(
            name="Demo News Organization"
        )
        publisher_org.editors.add(editor)
        publisher_org.journalists.add(journalist)
        print(f"Created publisher organization: {publisher_org.name}")
        
        # Create sample article
        article = Article.objects.create(
            title="Breaking: Django News App Launched!",
            content="""
            We are excited to announce the launch of our new Django-powered news application!
            
            This comprehensive platform provides:
            - Role-based user management
            - Editorial workflow with approval process
            - Subscription management for readers
            - RESTful API for third-party integration
            - Email notifications via Django signals
            - X/Twitter integration for social media sharing
            
            The application demonstrates professional-level Django development with:
            - PEP 8 compliant code
            - Comprehensive unit testing
            - Defensive programming practices
            - MariaDB database integration
            - Modern responsive UI
            
            Stay tuned for more exciting news and updates!
            """,
            author=journalist,
            publisher=publisher_org,
            status=Article.STATUS_PENDING
        )
        print(f"Created sample article: {article.title}")
        
        # Create sample newsletter
        newsletter = Newsletter.objects.create(
            title="Welcome to Our News Platform",
            content="""
            Dear Subscribers,
            
            Welcome to our new news platform! We're thrilled to have you as part of our community.
            
            What you can expect:
            - High-quality journalism from our team of professional journalists
            - Breaking news updates delivered directly to your inbox
            - In-depth analysis and exclusive interviews
            - Topics covering technology, business, politics, and more
            
            Our editorial team works around the clock to bring you accurate, timely, and engaging content.
            
            Thank you for your subscription and trust in our platform.
            
            Best regards,
            The Editorial Team
            """,
            journalist=journalist,
            publisher=publisher_org,
            approved=False
        )
        print(f"Created sample newsletter: {newsletter.title}")
        
        # Set up reader subscription
        reader.subscriptions_publishers.add(publisher_org)
        reader.subscriptions_journalists.add(journalist)
        print(f"Set up subscriptions for {reader.username}")
        
        print("\nDemo data created successfully!")
        print("\nLogin credentials:")
        print("Reader: demo_reader / demo123")
        print("Journalist: demo_journalist / demo123")
        print("Editor: demo_editor / demo123")
        print("Publisher: demo_publisher / demo123")
        
        print("\nNext steps:")
        print("1. Login as editor and approve the pending article")
        print("2. Login as reader to see the approved content")
        print("3. Test the API endpoints with the provided credentials")
        print("4. Check email notifications in the console")
        
    except Exception as e:
        print(f"Error creating demo data: {e}")


def cleanup_demo_data():
    """Remove demo data."""
    print("Cleaning up demo data...")
    try:
        CustomUser.objects.filter(username__startswith="demo_").delete()
        Publisher.objects.filter(name__contains="Demo").delete()
        Article.objects.filter(title__contains="Django News App").delete()
        Newsletter.objects.filter(title__contains="Welcome to Our").delete()
        print("Demo data cleaned up successfully!")
    except Exception as e:
        print(f"Error cleaning up demo data: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup_demo_data()
    else:
        create_demo_data()
