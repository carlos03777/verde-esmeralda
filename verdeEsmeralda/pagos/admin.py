from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "orden", "monto", "estado", "creado")
    list_filter = ("estado", "creado")
    search_fields = ("referencia", "wompi_id")