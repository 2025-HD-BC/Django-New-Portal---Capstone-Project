from django.urls import path, include
from . import views
from .views import RoleBasedLoginView, MyLogoutView, ArticleDeleteView, signup

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", signup, name="signup"),

    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("subscriptions/", views.subscriptions_view, name="subscriptions"),

    path("article/create/", views.article_create, name="article_create"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
    path("article/<int:pk>/approve/", views.article_approve, name="article_approve"),
    path("article/<int:pk>/reject/", views.article_reject, name="article_reject"),
    path("article/<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),

    path("subscribe/publisher/<int:publisher_id>/", views.subscribe_publisher, name="subscribe_publisher"),
    path("unsubscribe/publisher/<int:publisher_id>/", views.unsubscribe_publisher, name="unsubscribe_publisher"),
    path("subscribe/journalist/<int:journalist_id>/", views.subscribe_journalist, name="subscribe_journalist"),
    path("unsubscribe/journalist/<int:journalist_id>/", views.unsubscribe_journalist, name="unsubscribe_journalist"),

    path("publishers/", views.publishers_public_list, name="publishers_public_list"),
    path("publishers/manage/", views.publisher_list, name="publisher_list"),
    path("publishers/create/", views.publisher_create, name="publisher_create"),
    path("publishers/<int:pk>/", views.publisher_detail, name="publisher_detail"),
    path("publishers/<int:pk>/edit/", views.publisher_edit, name="publisher_edit"),
    path("publishers/<int:pk>/delete/", views.publisher_delete, name="publisher_delete"),

    # Newsletter URLs
    path("newsletters/", views.newsletter_list, name="newsletter_list"),
    path("newsletter/create/", views.newsletter_create, name="newsletter_create"),
    path("newsletter/<int:pk>/", views.newsletter_detail, name="newsletter_detail"),
    path("newsletter/<int:pk>/approve/", views.newsletter_approve, name="newsletter_approve"),
    path("newsletter/<int:pk>/reject/", views.newsletter_reject, name="newsletter_reject"),
    path("newsletter/<int:pk>/edit/", views.newsletter_edit, name="newsletter_edit"),

    # Error testing URLs (development only)
    path("template-test/", views.template_test, name="template_test"),
    path("error-test/", views.error_test, name="error_test"),
    path("test-403/", views.test_403, name="test_403"),
    path("test-500/", views.test_500, name="test_500"),

    path("api/", include("news.api.urls")),
]
