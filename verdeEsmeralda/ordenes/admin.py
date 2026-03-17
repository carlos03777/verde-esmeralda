from django.contrib import admin
from .models import Orden, OrdenItem, Direccion, Seguimiento


# =============================
# ITEMS DE ORDEN
# =============================

class OrdenItemInline(admin.TabularInline):

    model = OrdenItem

    extra = 0

    readonly_fields = (
        "producto",
        "price",
        "quantity",
    )


# =============================
# ORDEN
# =============================

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "total_formatted",
        "numero_productos",
        "estado",
        "creado",
    )

    list_filter = (
        "estado",
        "creado",
    )

    search_fields = (
        "id",
        "user__username",
        "user__email",
    )

    ordering = ("-creado",)

    readonly_fields = ("creado",)

    list_editable = ("estado",)

    inlines = [OrdenItemInline]


    # -------- total bonito --------

    def total_formatted(self, obj):
        return f"${obj.total}"

    total_formatted.short_description = "Total"


    # -------- número de productos --------

    def numero_productos(self, obj):
        return obj.ordenitem_set.count()

    numero_productos.short_description = "Productos"


# =============================
# DIRECCIONES
# =============================

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "usuario",
        "celular",
        "ciudad",
        "departamento",
        "direccion",
    )

    list_filter = (
        "ciudad",
        "departamento",
    )

    search_fields = (
        "nombre",
        "usuario__username",
        "celular",
        "ciudad",
    )

    ordering = ("-creado",)


# =============================
# SEGUIMIENTO
# =============================

@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):

    list_display = (
        "orden",
        "transportadora",
        "numeroSeguimiento",
        "estado",
        "fechaEnvio",
        "fechaEntrega",
    )

    list_filter = (
        "estado",
        "transportadora",
    )

    search_fields = (
        "numeroSeguimiento",
        "orden__id",
    )