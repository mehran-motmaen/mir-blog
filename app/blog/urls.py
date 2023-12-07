from django.urls import path
from django.views.generic import TemplateView

from .views import ArticleListView, ArticleDetailView, ContactView

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path(
        "articles/<slug:slug>-<int:pk>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path("contact/", ContactView.as_view(), name="contact_form"),
    path(
        "contact/success/",
        TemplateView.as_view(template_name="contact_success.html"),
        name="contact_success.html",
    ),
]
