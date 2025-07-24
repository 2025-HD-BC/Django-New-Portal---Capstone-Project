from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Article, Publisher, CustomUser, Newsletter
from .forms import (
    ArticleForm, CustomUserSignupForm, ProfileEditForm, PublisherForm, NewsletterForm
)
from .constants import UserRoles, ArticleStatus, Pagination

# --- ROLE TEST HELPERS ---
def is_editor(user):
    return user.is_authenticated and (user.role == UserRoles.EDITOR or user.groups.filter(name=UserRoles.EDITOR).exists())

def is_journalist(user):
    return user.is_authenticated and (user.role == UserRoles.JOURNALIST or user.groups.filter(name=UserRoles.JOURNALIST).exists())

def is_reader(user):
    return user.is_authenticated and (user.role == UserRoles.READER or user.groups.filter(name=UserRoles.READER).exists())

def is_publisher(user):
    return user.is_authenticated and (user.role == UserRoles.PUBLISHER or user.groups.filter(name=UserRoles.PUBLISHER).exists())

# --- HOME / PUBLIC ARTICLES ---
def home(request):
    articles = Article.objects.filter(status=ArticleStatus.APPROVED)
    return render(request, "news/article_list.html", {"articles": articles})

# --- USER PROFILE ---
@login_required
def profile_view(request):
    return render(request, "news/profile.html", {"user": request.user})

@login_required
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=user)
    return render(request, "news/profile_edit.html", {"form": form})

# --- DASHBOARD (ROLE BASED) ---
@login_required
def dashboard(request):
    """
    Role-based dashboard displaying relevant information for each user type.
    """
    user = request.user
    context = {}
    
    if is_reader(user):
        context = _get_reader_dashboard_context(user)
    elif is_journalist(user):
        context = _get_journalist_dashboard_context(user)
    elif is_editor(user):
        context = _get_editor_dashboard_context(user)
    elif is_publisher(user):
        context = _get_publisher_dashboard_context(user)
    
    # Add global stats
    context.update({
        "articles_count": Article.objects.count(),
        "publishers_count": Publisher.objects.count(),
    })
    
    return render(request, "news/dashboard.html", context)


def _get_reader_dashboard_context(user):
    """Helper function to get dashboard context for readers."""
    subscriptions_publishers = user.subscriptions_publishers.all()
    subscriptions_journalists = user.subscriptions_journalists.all()
    
    # Get articles from subscribed publishers and journalists
    publisher_articles = Article.objects.filter(
        status=ArticleStatus.APPROVED, 
        publisher__in=subscriptions_publishers
    )
    journalist_articles = Article.objects.filter(
        status=ArticleStatus.APPROVED, 
        author__in=subscriptions_journalists
    )
    articles = (publisher_articles | journalist_articles).distinct()
    
    return {
        "subscriptions_publishers": subscriptions_publishers,
        "subscriptions_journalists": subscriptions_journalists,
        "articles": articles,
        "newsletters": Newsletter.objects.filter(approved=True),
        "all_publishers": Publisher.objects.all(),
        "all_journalists": CustomUser.objects.filter(role="journalist"),
    }


def _get_journalist_dashboard_context(user):
    """Helper function to get dashboard context for journalists."""
    return {
        "my_articles": Article.objects.filter(author=user).order_by('-created_at'),
        "my_newsletters": Newsletter.objects.filter(journalist=user).order_by('-created_at'),
        "rejected_articles": Article.objects.filter(
            author=user, 
            status=Article.STATUS_REJECTED
        ),
    }


def _get_editor_dashboard_context(user):
    """Helper function to get dashboard context for editors."""
    return {
        "pending_articles": Article.objects.filter(status=ArticleStatus.PENDING),
        "rejected_articles": Article.objects.filter(
            status=ArticleStatus.REJECTED
        ).order_by('-reviewed_at')[:10],
        "pending_newsletters": Newsletter.objects.filter(
            approved=False
        ).order_by('-created_at'),
    }


def _get_publisher_dashboard_context(user):
    """Helper function to get dashboard context for publishers."""
    my_publishers = Publisher.objects.filter(editors=user)
    return {
        "my_publishers": my_publishers,
        "publisher_articles": Article.objects.filter(publisher__in=my_publishers),
    }

# --- ARTICLE CRUD & MODERATION ---
@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    user = request.user
    can_view_unapproved = (
        is_editor(user)
        or (is_publisher(user) and article.publisher and user in article.publisher.editors.all())
        or (user == article.author)
    )
    if article.status != ArticleStatus.APPROVED and not can_view_unapproved:
        raise PermissionDenied("You do not have permission to view this article.")
    return render(request, "news/article_detail.html", {"article": article})

@login_required
@user_passes_test(is_journalist)
def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            art = form.save(commit=False)
            art.author = request.user
            art.status = ArticleStatus.PENDING
            art.save()
            messages.success(request, "Article submitted for editorial review.")
            return redirect("dashboard")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ArticleForm()
    return render(request, "news/article_form.html", {"form": form})

@login_required
@user_passes_test(is_editor)
def article_approve(request, pk):
    # First, check if article exists at all
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        messages.error(request, f"Article with ID {pk} does not exist.")
        return redirect("dashboard")
    
    # Check if article is already approved or rejected
    if article.status == ArticleStatus.APPROVED:
        messages.warning(request, "Article is already approved.")
        return redirect("dashboard")
    elif article.status == ArticleStatus.REJECTED:
        messages.warning(request, "Article was previously rejected. Cannot approve rejected article.")
        return redirect("dashboard")
    elif article.status != ArticleStatus.PENDING:
        messages.error(request, f"Article status is '{article.status}'. Can only approve pending articles.")
        return redirect("dashboard")
    
    if request.method == "POST":
        article.approve(request.user)
        messages.success(request, f"Article '{article.title}' approved successfully.")
        return redirect("dashboard")
    return render(request, "news/article_approve.html", {"article": article})

@login_required
@user_passes_test(is_editor)
def article_reject(request, pk):
    # First, check if article exists at all
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        messages.error(request, f"Article with ID {pk} does not exist.")
        return redirect("dashboard")
    
    # Check if article is already approved or rejected
    if article.status == ArticleStatus.REJECTED:
        messages.warning(request, "Article is already rejected.")
        return redirect("dashboard")
    elif article.status == ArticleStatus.APPROVED:
        messages.warning(request, "Article was previously approved. Cannot reject approved article.")
        return redirect("dashboard")
    elif article.status != ArticleStatus.PENDING:
        messages.error(request, f"Article status is '{article.status}'. Can only reject pending articles.")
        return redirect("dashboard")
    
    if request.method == "POST":
        reason = request.POST.get("rejection_reason", "").strip()
        if not reason:
            messages.error(request, "Please provide a rejection reason.")
            return render(request, "news/article_reject.html", {"article": article})
        article.reject(request.user, reason)
        messages.success(request, f"Article '{article.title}' rejected.")
        return redirect("dashboard")
    return render(request, "news/article_reject.html", {"article": article})

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "news/article_delete.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        user = self.request.user
        article = self.get_object()
        if getattr(user, "role", None) == UserRoles.EDITOR:
            return True
        if getattr(user, "role", None) == UserRoles.JOURNALIST and article.author == user:
            return article.status == ArticleStatus.PENDING
        return False

# --- READER SUBSCRIPTIONS ---
@login_required
@user_passes_test(is_reader)
def subscribe_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    request.user.subscriptions_publishers.add(publisher)
    messages.success(request, f"You have subscribed to {publisher.name}.")
    return redirect("dashboard")

@login_required
@user_passes_test(is_reader)
def unsubscribe_publisher(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    request.user.subscriptions_publishers.remove(publisher)
    messages.info(request, f"You have unsubscribed from {publisher.name}.")
    return redirect("dashboard")

@login_required
@user_passes_test(is_reader)
def subscribe_journalist(request, journalist_id):
    journalist = get_object_or_404(CustomUser, pk=journalist_id, role="journalist")
    request.user.subscriptions_journalists.add(journalist)
    messages.success(request, f"You have subscribed to {journalist.username}.")
    return redirect("dashboard")

@login_required
@user_passes_test(is_reader)
def unsubscribe_journalist(request, journalist_id):
    journalist = get_object_or_404(CustomUser, pk=journalist_id, role="journalist")
    request.user.subscriptions_journalists.remove(journalist)
    messages.info(request, f"You have unsubscribed from {journalist.username}.")
    return redirect("dashboard")

@login_required
@user_passes_test(is_reader)
def subscriptions_view(request):
    """View for managing reader subscriptions"""
    user = request.user
    total_subscriptions = user.subscriptions_publishers.count() + user.subscriptions_journalists.count()
    
    context = {
        'total_subscriptions': total_subscriptions,
    }
    return render(request, "news/subscriptions.html", context)

# --- USER SIGNUP / LOGIN / LOGOUT ---
def signup(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful. Welcome!")
            return redirect("home" if user.role == "reader" else "dashboard")
        messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserSignupForm()
    return render(request, "registration/signup.html", {"form": form})

class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        return "/" if user.role == "reader" else "/dashboard/"

class MyLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
    next_page = '/'  # Redirect to home page after logout

    # --- PUBLISHER MANAGEMENT ---

@login_required
@user_passes_test(is_publisher)
@login_required
def publisher_list(request):
    """Management view for publishers to see their own organizations"""
    publishers = Publisher.objects.filter(editors=request.user)
    return render(request, "news/publisher_list.html", {"publishers": publishers})

def publishers_public_list(request):
    """Public view for all readers to browse and subscribe to publishers"""
    publishers = Publisher.objects.all().order_by('name')
    return render(request, "news/publisher_list_public.html", {"publishers": publishers})

@login_required
def publisher_create(request):
    # Allow editors and publishers to create publisher organizations
    if not (request.user.role in ["editor", "publisher"] or 
            request.user.groups.filter(name__in=["editor", "publisher"]).exists()):
        messages.error(request, "You need editor or publisher permissions to create a publisher organization.")
        return redirect("dashboard")
        
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save(commit=False)
            publisher.save()
            publisher.editors.add(request.user)
            messages.success(request, "Publisher created successfully.")
            return redirect("publisher_list")
        messages.error(request, "Please correct the errors below.")
    else:
        form = PublisherForm()
    return render(request, "news/publisher_form.html", {"form": form})

@login_required
@user_passes_test(is_publisher)
def publisher_detail(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk, editors=request.user)
    return render(request, "news/publisher_detail.html", {"publisher": publisher})

@login_required
@user_passes_test(is_publisher)
def publisher_edit(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk, editors=request.user)
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request, "Publisher updated successfully.")
            return redirect("publisher_detail", pk=pk)
        messages.error(request, "Please correct the errors below.")
    else:
        form = PublisherForm(instance=publisher)
    return render(request, "news/publisher_form.html", {"form": form})

@login_required
@user_passes_test(is_publisher)
def publisher_delete(request, pk):
    publisher = get_object_or_404(Publisher, pk=pk, editors=request.user)
    if request.method == "POST":
        publisher.delete()
        messages.success(request, "Publisher deleted.")
        return redirect("publisher_list")
    return render(request, "news/publisher_confirm_delete.html", {"publisher": publisher})


# --- NEWSLETTER CRUD ---
@login_required
@user_passes_test(is_journalist)
def newsletter_create(request):
    """Allow journalists to create newsletters."""
    if request.method == "POST":
        form = NewsletterForm(request.POST, user=request.user)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.journalist = request.user
            newsletter.approved = False  # Needs editor approval
            newsletter.save()
            messages.success(request, "Newsletter submitted for editorial review.")
            return redirect("dashboard")
        messages.error(request, "Please correct the errors below.")
    else:
        form = NewsletterForm(user=request.user)
    return render(request, "news/newsletter_form.html", {"form": form})


def newsletter_list(request):
    """Display all approved newsletters."""
    newsletters = Newsletter.objects.filter(approved=True).order_by('-created_at')
    return render(request, "news/newsletter_list.html", {"newsletters": newsletters})


@login_required
def newsletter_detail(request, pk):
    """View newsletter details."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    user = request.user
    
    # Check permissions - readers can only see approved newsletters
    # Journalists can see their own, editors can see all
    can_view_unapproved = (
        is_editor(user) or 
        (newsletter.journalist == user)
    )
    
    if not newsletter.approved and not can_view_unapproved:
        raise PermissionDenied("You do not have permission to view this newsletter.")
    
    return render(request, "news/newsletter_detail.html", {"newsletter": newsletter})


@login_required
@user_passes_test(is_editor)
def newsletter_approve(request, pk):
    """Allow editors to approve newsletters."""
    newsletter = get_object_or_404(Newsletter, pk=pk, approved=False)
    if request.method == "POST":
        newsletter.approved = True
        newsletter.save()
        messages.success(request, "Newsletter approved and published.")
        return redirect("dashboard")
    return render(request, "news/newsletter_approve.html", {"newsletter": newsletter})


@login_required
@user_passes_test(is_editor)
def newsletter_reject(request, pk):
    """Allow editors to reject newsletters."""
    newsletter = get_object_or_404(Newsletter, pk=pk, approved=False)
    if request.method == "POST":
        # For now, we'll just delete rejected newsletters
        # In a full implementation, you might want to add a rejection reason field
        newsletter.delete()
        messages.info(request, "Newsletter rejected and removed.")
        return redirect("dashboard")
    return render(request, "news/newsletter_reject.html", {"newsletter": newsletter})


@login_required
def newsletter_edit(request, pk):
    """Allow journalists to edit their own newsletters (if not yet approved)."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    user = request.user
    
    # Only allow editing by the author and only if not yet approved
    if newsletter.journalist != user or newsletter.approved:
        raise PermissionDenied("You cannot edit this newsletter.")
    
    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully.")
            return redirect("newsletter_detail", pk=pk)
        messages.error(request, "Please correct the errors below.")
    else:
        form = NewsletterForm(instance=newsletter, user=user)
    
    return render(request, "news/newsletter_form.html", {"form": form, "newsletter": newsletter})


# --- CUSTOM ERROR HANDLERS ---
def custom_403(request, exception):
    """Custom 403 error handler"""
    return render(request, "403.html", status=403)


def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, "404.html", status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, "500.html", status=500)


# --- ERROR TESTING VIEWS (DEVELOPMENT ONLY) ---
def template_test(request):
    """View to test template loading"""
    return render(request, "news/template_test.html")


def error_test(request):
    """View to test error pages - only for development"""
    from django.conf import settings
    if not settings.DEBUG:
        raise PermissionDenied("Error testing only available in debug mode")
    return render(request, "news/error_test.html")


def test_403(request):
    """Test view to trigger 403 error"""
    from django.conf import settings
    if not settings.DEBUG:
        raise PermissionDenied("Error testing only available in debug mode")
    raise PermissionDenied("This is a test 403 error")


def test_500(request):
    """Test view to trigger 500 error"""
    from django.conf import settings
    if not settings.DEBUG:
        raise PermissionDenied("Error testing only available in debug mode")
    raise Exception("This is a test 500 error")

