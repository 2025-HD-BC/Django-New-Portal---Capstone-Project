"""
DRF API integration tests (aligned with Article.status and plain‑list responses)
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from news.models import (
    Article,
    Publisher,
    Subscription,
    CustomUser,
)


class APIMixins:
    password = "test-pass-123"

    def _create_user(self, username, role, **kwargs):
        return CustomUser.objects.create_user(
            username=username,
            password=self.password,
            role=role,
            email=f"{username}@example.com",
            **kwargs,
        )

    def _auth(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client


# LIST / DETAIL TESTS
class ArticleListDetailTests(APIMixins, APITestCase):
    def setUp(self):
        self.reader = self._create_user("reader", "reader")
        self.journalist = self._create_user("writer", "journalist")

        self.article = Article.objects.create(
            title="Approved piece",
            content="Lorem ipsum…",
            author=self.journalist,
            status=Article.STATUS_APPROVED,
        )

        self.list_url = reverse("api-article-list")
        self.detail_url = reverse("api-article-detail", args=[self.article.pk])

    def test_reader_sees_article_list(self):
        res = self._auth(self.reader).get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)          # plain list response

    def test_reader_sees_article_detail(self):
        res = self._auth(self.reader).get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.article.pk)


# APPROVAL TESTS
class ArticleApprovalTests(APIMixins, APITestCase):
    def setUp(self):
        self.editor = self._create_user("ed", "editor", is_staff=True)
        self.journalist = self._create_user("jj", "journalist")

        self.article = Article.objects.create(
            title="Needs approval",
            content="Draft…",
            author=self.journalist,
            status=Article.STATUS_PENDING,
        )

        self.approve_url = reverse("api-article-approve", args=[self.article.pk])

    def test_editor_can_approve_article(self):
        res = self._auth(self.editor).post(self.approve_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertTrue(self.article.is_approved)

    def test_reader_cannot_approve_article(self):
        reader = self._create_user("joe", "reader")
        res = self._auth(reader).post(self.approve_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.article.refresh_from_db()
        self.assertFalse(self.article.is_approved)


# SUBSCRIPTION FEED TESTS
class SubscriptionFeedTests(APIMixins, APITestCase):
    def setUp(self):
        self.reader = self._create_user("subby", "reader")
        self.publisher = Publisher.objects.create(name="Daily Planet")

        Subscription.objects.create(reader=self.reader, publisher=self.publisher)

        journalist = self._create_user("lois", "journalist")

        # Approved article – should appear in feed
        self.good_article = Article.objects.create(
            title="Hello Metropolis",
            content="City news…",
            author=journalist,
            publisher=self.publisher,
            status=Article.STATUS_APPROVED,
        )

        # Pending article – should NOT appear
        Article.objects.create(
            title="Draft",
            content="Unpublished…",
            author=journalist,
            publisher=self.publisher,
            status=Article.STATUS_PENDING,
        )

        self.feed_url = reverse("api-subscription-feed")

    def test_feed_returns_only_approved_articles_from_subscriptions(self):
        res = self._auth(self.reader).get(self.feed_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ids = [art["id"] for art in res.data]       # plain list response
        self.assertEqual(ids, [self.good_article.pk])
