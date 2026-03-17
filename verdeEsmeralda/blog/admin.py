from django.contrib import admin
from .models import Post, PostCategory


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "titulo",
        "categoria",
        "publicado",
        "creado",
    )

    list_filter = (
        "publicado",
        "categoria",
        "creado",
    )

    search_fields = (
        "titulo",
        "contenido",
    )

    prepopulated_fields = {"slug": ("titulo",)}

    ordering = ("-creado",)


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):

    list_display = ("nombre",)

    search_fields = ("nombre",)

    prepopulated_fields = {"slug": ("nombre",)}