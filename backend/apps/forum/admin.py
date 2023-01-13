from django.contrib import admin

from apps.forum.models import Category, Post, Reply


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "slug",
    )
    search_fields = ("title", "author__name")
    list_filter = ("category",)
    ordering = ("created_at",)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "parent",
        "author",
        "created_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = ("author__name",)
