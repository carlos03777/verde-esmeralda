from django.contrib import admin
from .models import Pagos


@admin.register(Pagos)
class PagosAdmin(admin.ModelAdmin):

    list_display = (
        "orden",
        "metodo",
        "cantidad",
        "estado",
        "creado",
    )

    list_filter = (
        "metodo",
        "estado",
        "creado",
    )

    search_fields = (
        "orden__id",
    )

    ordering = ("-creado",)

    readonly_fields = ("creado",)