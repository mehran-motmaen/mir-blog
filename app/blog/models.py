from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Article(models.Model):
    """
    Represents a blog article.

    Attributes:
        title (str): The title of the article.
        slug (str): The URL-friendly version of the title (prepopulated from title).
        content (str): The content of the article.
        author (User): The author of the article (foreign key to User model).
        publication_datetime (datetime): The date and time when the article was published.
        is_online (bool): Indicates whether the article is online or offline.
    """

    title = models.CharField(
        max_length=255, help_text="Enter the title of the article."
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="A URL-friendly version of the title, automatically generated from the title.",
    )
    content = models.TextField(help_text="Enter the content of the article.")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Select the author of the article.",
    )
    publication_datetime = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the article was published.",
    )
    is_online = models.BooleanField(
        default=True,
        help_text="Check to make the article available online; uncheck to take it offline.",
    )

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically generate the slug from the title.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContactRequest(models.Model):
    """
    Represents a contact request.

    Attributes:
        email (str): The email address of the contact requester.
        name (str): The name of the contact requester.
        content (str): The content of the contact request.
        date (datetime): The date and time when the contact request was made.
    """

    email = models.EmailField(help_text="Enter your email address.")
    name = models.CharField(max_length=255, help_text="Enter your name.")
    content = models.TextField(help_text="Enter the content of your contact request.")
    date = models.DateTimeField(
        auto_now_add=True, help_text="The date and time of the contact request."
    )

    def __str__(self):
        return f"Contact Request from {self.name}"
