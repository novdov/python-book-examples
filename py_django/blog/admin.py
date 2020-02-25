from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "modify_dt")
    list_filter = ("modify_dt",)
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    @staticmethod
    def tag_list(obj):
        return ", ".join(o.name for o in obj.tag.all())
