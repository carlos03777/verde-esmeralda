from django.contrib import admin
from .models import Nosotros, Equipo, Contacto,  MensajeContacto, Taller


# ======================================
# NOSOTROS (ANTES FUNDADORA)
# ======================================
@admin.register(Nosotros)
class NosotrosAdmin(admin.ModelAdmin):

    list_display = ("titulo", "actualizado")
    search_fields = ("titulo", "descripcion")

    fieldsets = (
        ("Información principal", {
            "fields": ("titulo", "descripcion", "imagen")
        }),
        ("Contenido adicional", {
            "fields": ("historia", "frase"),
            "classes": ("collapse",)
        }),
    )


# ======================================
#  EQUIPO
# ======================================
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):

    list_display = ("nombre", "cargo", "activo", "orden")
    list_filter = ("activo",)
    search_fields = ("nombre", "cargo")

    fieldsets = (
        ("Información", {
            "fields": ("nombre", "cargo", "foto")
        }),
        ("Contenido", {
            "fields": ("descripcion",)
        }),
        ("Configuración", {
            "fields": ("activo", "orden")
        }),
    )



@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "email", "telefono")


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "leido", "creado")
    list_filter = ("leido",)
    search_fields = ("nombre", "email")
    list_editable = ("leido",)


from .models import ConfiguracionSitio

@admin.register(ConfiguracionSitio)
class ConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ConfiguracionSitio.objects.exists()
    


@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "precio", "activo", "destacado")
    list_filter = ("activo", "destacado", "fecha")
    search_fields = ("titulo",)
    prepopulated_fields = {"slug": ("titulo",)}