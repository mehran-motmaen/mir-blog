from django.contrib import admin
from .models import Article, ContactRequest

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_datetime', 'is_online')
    list_filter = ('is_online',)
    search_fields = ('title', 'author__username')

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'date')
    readonly_fields = ('email', 'name', 'content', 'date')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
