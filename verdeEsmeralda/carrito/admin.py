from django.contrib import admin
from .models import Carrito, CarritoItem


class CarritoItemInline(admin.TabularInline):
    model = CarritoItem
    extra = 0


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "usuario",
        "creado",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
    )

    ordering = ("-creado",)

    inlines = [CarritoItemInline]