from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Article
from django.utils import timezone
from django.test.client import Client
from django.core.paginator import Paginator


class ArticleModelTest(TestCase):
    """
    Test cases for the Article model.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        self.user = User.objects.create_user(
            username="Mehran",
            password="testpassword",
        )
        self.article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author=self.user,
        )

    def test_article_creation(self):
        """
        Test the creation of an article instance.
        """
        self.assertEqual(
            self.article.title,
            "Test Article",
        )
        self.assertEqual(
            self.article.content,
            "Test content",
        )
        self.assertEqual(
            self.article.author,
            self.user,
        )
        self.assertIsNotNone(self.article.slug)

    def test_str_representation(self):
        """
        Test the string representation of the article.
        """
        self.assertEqual(
            str(self.article),
            "Test Article",
        )


class ArticleAdminTest(TestCase):
    """
    Test cases for the Article admin.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        self.admin_user = User.objects.create_user(
            username="admin",
            password="adminpassword",
            is_staff=True,
            is_superuser=True,
        )
        self.client = Client()
        self.client.login(
            username="admin",
            password="adminpassword",
        )

    def test_article_admin_list_display(self):
        """
        Test the list display in the Article admin.
        """
        article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            author=self.admin_user,
            publication_datetime=timezone.now(),
            is_online=True,
        )

        response = self.client.get(reverse("admin:blog_article_changelist"))
        self.assertContains(
            response,
            "Test Article",
        )
        self.assertContains(
            response,
            "admin",
        )
        self.assertContains(
            response,
            True,
        )

    def test_article_admin_search(self):
        """
        Test the search functionality in the Article admin.
        """
        article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            author=self.admin_user,
            publication_datetime=timezone.now(),
            is_online=True,
        )

        response = self.client.get(
            reverse("admin:blog_article_changelist"),
            {"q": "Test Article"},
        )
        self.assertContains(
            response,
            "Test Article",
        )
        self.assertContains(
            response,
            "admin",
        )

    def test_article_admin_filter(self):
        """
        Test the filtering in the Article admin.
        """
        article = Article.objects.create(
            title="Test Article",
            content="This is a test article content.",
            author=self.admin_user,
            publication_datetime=timezone.now(),
            is_online=True,
        )

        response = self.client.get(
            reverse("admin:blog_article_changelist"),
            {"is_online": "1"},
        )
        self.assertContains(
            response,
            "Test Article",
        )
        self.assertContains(
            response,
            "admin",
        )


class ArticleListViewTest(TestCase):
    """
    Test cases for the Article list view.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.online_article = Article.objects.create(
            title="TestArticleOnline",
            content="Test content",
            author=self.user,
            is_online=True,
        )
        self.offline_article = Article.objects.create(
            title="TestArticleOffline",
            content="Test content",
            author=self.user,
            is_online=False,
        )

    def test_article_list_view(self):
        """
        Test the Article list view.
        """
        response = self.client.get(reverse("article_list"))
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertTemplateUsed(
            response,
            "article_list.html",
        )

        # Check that the online article is present in the response context
        self.assertIn(
            self.online_article,
            response.context["articles"],
        )

        # Check that the offline article is not present in the response context
        self.assertNotIn(
            self.offline_article,
            response.context["articles"],
        )

        # Check pagination
        paginator = Paginator(
            response.context["articles"],
            5,
        )
        self.assertEqual(
            paginator.num_pages,
            1,
        )  # Since we only have one online article


class ArticleDetailViewTest(TestCase):
    """
    Test cases for the Article detail view.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.online_article = Article.objects.create(
            title="TestArticleOnline",
            content="Test content",
            author=self.user,
            is_online=True,
        )
        self.offline_article = Article.objects.create(
            title="TestArticleOffline",
            content="Test content",
            author=self.user,
            is_online=False,
        )

    def test_online_article_detail_view(self):
        """
        Test the Article detail view for an online article.
        """
        response = self.client.get(
            reverse(
                "article_detail",
                kwargs={
                    "slug": self.online_article.slug,
                    "pk": self.online_article.id,
                },
            )
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertTemplateUsed(
            response,
            "article_detail.html",
        )
        self.assertEqual(
            response.context["article"],
            self.online_article,
        )

    def test_offline_article_detail_view(self):
        """
        Test that accessing the detail view for an offline article returns a 404 status code.
        """
        response = self.client.get(
            reverse(
                "article_detail",
                kwargs={
                    "slug": self.offline_article.slug,
                    "pk": self.offline_article.id,
                },
            )
        )
        self.assertEqual(
            response.status_code,
            404,
        )
