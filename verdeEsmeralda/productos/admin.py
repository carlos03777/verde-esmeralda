from django.contrib import admin
from .models import Categoria, Producto, ImagenProducto


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "categoria",
        "precio",
        "stock",
        "disponible",
        "creado",
    )

    list_filter = (
        "categoria",
        "disponible",
        "creado",
    )

    search_fields = (
        "nombre",
        "descripcion",
    )

    prepopulated_fields = {"slug": ("nombre",)}

    inlines = [ImagenProductoInline]

    ordering = ("-creado",)

    list_editable = ("precio", "stock", "disponible")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = ("nombre", "slug")

    search_fields = ("nombre",)

    prepopulated_fields = {"slug": ("nombre",)}