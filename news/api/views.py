# news/api/views.py
from django.utils import timezone
from rest_framework import permissions, viewsets, generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from news.models import (
    Article,
    Publisher,
    CustomUser,
    Newsletter,
    Subscription,          # ← NEW import
)
from news.constants import UserRoles, ArticleStatus
from .serializers import (
    ArticleSerializer,
    PublisherSerializer,
    CustomUserSerializer,
    NewsletterSerializer,
)

# ────────────────────────────────────────────────────────────────
#  EXTRA ENDPOINTS REQUIRED BY THE TEST SUITE
# ────────────────────────────────────────────────────────────────
class ArticleApproveView(APIView):
    """
    POST /api/articles/<pk>/approve/
    Editors only – set status to APPROVED and return the article.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if getattr(request.user, "role", None) != "editor":
            return Response({"detail": "Only editors can approve."}, status=status.HTTP_403_FORBIDDEN)

        article.approve(request.user)
        return Response(
            ArticleSerializer(article, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )


class SubscriptionFeedView(generics.ListAPIView):
    """
    GET /api/subscriptions/feed/
    Return approved articles from publishers and journalists
    the authenticated reader follows.
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) != "reader":
            return Article.objects.none()

        # Publisher IDs via Subscription model
        pub_ids = Subscription.objects.filter(reader=user).values_list(
            "publisher_id", flat=True
        )
        # Journalist IDs via the existing M2M (if any)
        jour_ids = user.subscriptions_journalists.values_list("id", flat=True)

        qs = (
            Article.objects.filter(status=ArticleStatus.APPROVED, publisher_id__in=pub_ids)
            | Article.objects.filter(status=ArticleStatus.APPROVED, author_id__in=jour_ids)
        )
        return qs.distinct().order_by("-created_at")

# ────────────────────────────────────────────────────────────────
#  EXISTING FEED‑STYLE FUNCTION VIEWS
# ────────────────────────────────────────────────────────────────
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_subscribed_articles(request):
    user = request.user
    if getattr(user, "role", None) != "reader":
        return Response({"detail": "Only readers can use this endpoint."}, status=403)

    pub_ids = Subscription.objects.filter(reader=user).values_list(
        "publisher_id", flat=True
    )
    jour_ids = user.subscriptions_journalists.values_list("id", flat=True)

    articles = (
        Article.objects.filter(status=ArticleStatus.APPROVED, publisher_id__in=pub_ids)
        | Article.objects.filter(status=ArticleStatus.APPROVED, author_id__in=jour_ids)
    ).distinct().order_by("-created_at")

    return Response(ArticleSerializer(articles, many=True, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_publisher_articles(request, publisher_id):
    articles = Article.objects.filter(
        status=ArticleStatus.APPROVED, publisher_id=publisher_id
    ).order_by("-created_at")
    return Response(ArticleSerializer(articles, many=True, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_journalist_articles(request, journalist_id):
    articles = Article.objects.filter(
        status=ArticleStatus.APPROVED, author_id=journalist_id
    ).order_by("-created_at")
    return Response(ArticleSerializer(articles, many=True, context={"request": request}).data)

# ────────────────────────────────────────────────────────────────
#  CRUD VIEWSETS
# ────────────────────────────────────────────────────────────────
class ArticleViewSet(viewsets.ModelViewSet):
    queryset           = Article.objects.all()
    serializer_class   = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != UserRoles.JOURNALIST:
            raise permissions.PermissionDenied("Only journalists can submit articles.")
        serializer.save(author=self.request.user, status=ArticleStatus.PENDING)

    def perform_update(self, serializer):
        article = self.get_object()
        new_status = self.request.data.get("status")

        if new_status in (ArticleStatus.APPROVED, ArticleStatus.REJECTED):
            if self.request.user.role != UserRoles.EDITOR:
                raise permissions.PermissionDenied("Only editors can approve/reject.")
            serializer.save(
                status=new_status,
                reviewed_by=self.request.user,
                reviewed_at=timezone.now(),
                rejection_reason=self.request.data.get("rejection_reason", ""),
            )
            return

        if self.request.user == article.author and article.status == ArticleStatus.PENDING:
            serializer.save()
        else:
            raise permissions.PermissionDenied("Cannot modify this article.")

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        if article.status == ArticleStatus.APPROVED:
            raise permissions.PermissionDenied("Cannot delete a published article.")
        return super().destroy(request, *args, **kwargs)


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Publisher.objects.all()
    serializer_class   = PublisherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = CustomUser.objects.all()
    serializer_class   = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset         = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]

        if self.action == "create":
            if self.request.user.is_authenticated and self.request.user.role == "journalist":
                return [IsAuthenticated()]
            raise exceptions.PermissionDenied("Only journalists can create newsletters.")

        if self.request.user.is_authenticated and self.request.user.role == "editor":
            return [IsAuthenticated()]
        raise exceptions.PermissionDenied("Only editors can modify newsletters.")

    def perform_create(self, serializer):
        serializer.save(journalist=self.request.user, approved=False)

    def perform_update(self, serializer):
        serializer.save(approved=self.request.data.get("approved", True))
