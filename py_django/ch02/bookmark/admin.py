from bookmark.models import Bookmark
from django.contrib import admin


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url")
