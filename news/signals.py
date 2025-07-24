# news/signals.py
import requests
from requests_oauthlib import OAuth1
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.mail.utils import DNS_NAME    # ← NEW
from decouple import config
from .models import Article, Newsletter, CustomUser


# ──────────────────────────────────────────────
# 1.  Add / move users to the correct role group
# ──────────────────────────────────────────────
@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    if kwargs.get("raw", False):
        return          # skip loaddata / fixture runs

    if instance.role:
        # remove from ANY existing role groups first
        for slug, _ in sender._meta.get_field("role").choices:
            grp = Group.objects.filter(name=slug).first()
            if grp and grp in instance.groups.all():
                instance.groups.remove(grp)

        # then pop them into the right one
        grp, _ = Group.objects.get_or_create(name=instance.role)
        instance.groups.add(grp)


# ──────────────────────────────────────────────
# 2.  Helper utilities
# ──────────────────────────────────────────────
def _subscriber_emails(publisher, journalist):
    """
    Collect a set of reader e‑mail addresses for a given publisher / journalist
    (ignore blank addresses automatically).
    """
    emails = set()

    if publisher:
        emails |= {u.email for u in publisher.subscribed_readers.all() if u.email}

    if journalist:
        emails |= {u.email for u in journalist.subscribers.all() if u.email}

    return emails


def _send_notification(recipients, subject, message):
    """
    Send the mail through Django’s *console* backend.
    On some Windows machines socket.getfqdn() returns an empty string, which
    crashes the console backend when it tries to build the Message‑ID header.
    We patch that once, right here.
    """
    if not recipients:
        return

    # ---- ONE‑LINE FIX FOR THE UNICODE / idna BUG ----
    if not getattr(DNS_NAME, "_fqdn", ""):
        DNS_NAME._fqdn = "localhost"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=list(recipients),
        fail_silently=not settings.DEBUG,
    )


def _post_to_x_twitter(content, article_link=None, image_path=None):
    """
    Post content to X (Twitter) using the HTTP API v2.
    Uses OAuth 1.0a User Context authentication.
    Supports image uploads.
    """
    import os
    from django.core.files.storage import default_storage
    
    # Get X API credentials from environment variables
    api_key = config("X_API_KEY", default="")
    api_secret = config("X_API_SECRET", default="")
    access_token = config("X_ACCESS_TOKEN", default="")
    access_token_secret = config("X_ACCESS_TOKEN_SECRET", default="")
    
    # For Twitter API v2, we need OAuth 1.0a User Context
    if not all([api_key, api_secret, access_token, access_token_secret]):
        if settings.DEBUG:
            print("[SIGNAL] X/Twitter posting skipped - OAuth 1.0a credentials not fully configured")
        return False
    
    try:
        # Set up OAuth 1.0a authentication
        auth = OAuth1(
            api_key,
            client_secret=api_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            signature_method='HMAC-SHA1',
            signature_type='AUTH_HEADER'
        )
        
        # Step 1: Upload media if image is provided
        media_id = None
        if image_path and os.path.exists(image_path):
            try:
                # Upload media using v1.1 API (required for media upload)
                with open(image_path, 'rb') as image_file:
                    files = {'media': image_file}
                    
                    media_response = requests.post(
                        'https://upload.twitter.com/1.1/media/upload.json',
                        auth=auth,
                        files=files,
                        timeout=30
                    )
                    
                    if media_response.status_code == 200:
                        media_data = media_response.json()
                        media_id = media_data.get('media_id_string')
                        if settings.DEBUG:
                            print(f"[SIGNAL] ✅ Successfully uploaded media (ID: {media_id})")
                    else:
                        if settings.DEBUG:
                            print(f"[SIGNAL] ⚠️ Failed to upload media: {media_response.status_code} - {media_response.text}")
                        
            except Exception as e:
                if settings.DEBUG:
                    print(f"[SIGNAL] ⚠️ Error uploading media: {e}")
        
        # Step 2: Prepare the tweet content (X has character limits - 280 characters)
        base_text = content[:200]  # Leave room for link and ellipsis
        
        if article_link:
            # Add link to the tweet
            tweet_text = f"{base_text} {article_link}"
        else:
            tweet_text = base_text
            
        # Truncate if still too long
        if len(tweet_text) > 280:
            tweet_text = f"{base_text[:250]}... {article_link}" if article_link else base_text[:280]
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'text': tweet_text
        }
        
        # Add media if uploaded successfully
        if media_id:
            data['media'] = {'media_ids': [media_id]}
        
        # Step 3: Create tweet using Twitter API v2 endpoint with OAuth 1.0a
        response = requests.post(
            'https://api.twitter.com/2/tweets',
            auth=auth,
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 201:
            tweet_data = response.json()
            tweet_id = tweet_data.get('data', {}).get('id', 'unknown')
            media_info = " with image" if media_id else ""
            if settings.DEBUG:
                print(f"[SIGNAL] ✅ Successfully posted to X (Tweet ID: {tweet_id}){media_info}: {tweet_text[:50]}...")
            return True
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            if settings.DEBUG:
                print(f"[SIGNAL] ❌ Failed to post to X. Status: {response.status_code}, Error: {error_data}")
            return False
            
    except Exception as e:
        if settings.DEBUG:
            print(f"[SIGNAL] ❌ Error posting to X: {e}")
        return False
# ──────────────────────────────────────────────
# 3.  Article approval → inform subscribers
# ──────────────────────────────────────────────
@receiver(post_save, sender=Article)
def notify_article_approval(sender, instance, created, **kwargs):
    if kwargs.get("raw", False) or created or instance.status != Article.STATUS_APPROVED:
        return

    recipients = _subscriber_emails(instance.publisher, instance.author)

    if settings.DEBUG:
        print(f"[SIGNAL] Article approved: {instance.title} – {len(recipients)} e‑mails")

    link = f"http://{settings.DOMAIN}/article/{instance.pk}/"
    subj = f"New Article: {instance.title}"
    msg = (
        f"{instance.author} published a new article.\n\n"
        f"{instance.content[:250]}...\n\nRead more: {link}"
    )
    _send_notification(recipients, subj, msg)
    
    # Also post to X/Twitter with image if available
    tweet_content = f"📰 New Article Published!\n\n🔥 {instance.title}\n✍️ By {instance.author.get_full_name() or instance.author.username}"
    if instance.publisher:
        tweet_content += f"\n🏢 {instance.publisher.name}"
    tweet_content += f"\n\n#News #Article"
    
    # Get the image path if article has an image
    image_path = None
    if instance.image and hasattr(instance.image, 'path'):
        try:
            image_path = instance.image.path
        except (ValueError, AttributeError):
            # Handle cases where image.path might not be accessible
            pass
    
    _post_to_x_twitter(tweet_content, link, image_path)


# ──────────────────────────────────────────────
# 4.  Newsletter approval → inform subscribers
# ──────────────────────────────────────────────
@receiver(post_save, sender=Newsletter)
def notify_newsletter_approval(sender, instance, created, **kwargs):
    if kwargs.get("raw", False) or created or not instance.approved:
        return

    recipients = _subscriber_emails(instance.publisher, instance.journalist)

    if settings.DEBUG:
        print(f"[SIGNAL] Newsletter approved: {instance.title} – {len(recipients)} e‑mails")

    link = f"http://{settings.DOMAIN}/newsletter/{instance.pk}/"
    subj = f"New Newsletter: {instance.title}"
    msg = (
        f"{instance.journalist} released a newsletter.\n\n"
        f"{instance.content[:250]}...\n\nRead more: {link}"
    )
    _send_notification(recipients, subj, msg)
    
    # Also post to X/Twitter with image if available
    tweet_content = f"📧 New Newsletter Released!\n\n📰 {instance.title}\n✍️ By {instance.journalist.get_full_name() or instance.journalist.username}"
    if instance.publisher:
        tweet_content += f"\n🏢 {instance.publisher.name}"
    tweet_content += f"\n\n#Newsletter #News"
    
    # Get the image path if newsletter has an image
    image_path = None
    if hasattr(instance, 'image') and instance.image and hasattr(instance.image, 'path'):
        try:
            image_path = instance.image.path
        except (ValueError, AttributeError):
            # Handle cases where image.path might not be accessible
            pass
    
    _post_to_x_twitter(tweet_content, link, image_path)
