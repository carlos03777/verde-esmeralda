from django.contrib import admin
from .models import (
    Nosotros,
    Equipo,
    Contacto,
    MensajeContacto,
    ConfiguracionSitio,
    Taller,
    Inscripcion,
    PaginaLegal,
)


# ======================================
# 🌿 NOSOTROS
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
# 👥 EQUIPO
# ======================================
@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):

    list_display = ("nombre", "cargo", "activo", "orden")
    list_filter = ("activo",)
    search_fields = ("nombre", "cargo")
    list_editable = ("activo", "orden")

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


# ======================================
# 📞 CONTACTO (INFO EMPRESA)
# ======================================
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):

    list_display = ("titulo", "email", "telefono", "actualizado")

    fieldsets = (
        ("Información", {
            "fields": ("titulo", "descripcion")
        }),
        ("Contacto", {
            "fields": ("email", "telefono", "direccion", "horario")
        }),
    )


# ======================================
# 📩 MENSAJES DE CONTACTO
# ======================================
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):

    list_display = ("nombre", "email", "leido", "creado")
    list_filter = ("leido", "creado")
    search_fields = ("nombre", "email", "mensaje")
    list_editable = ("leido",)

    readonly_fields = ("nombre", "email", "mensaje", "creado")

    ordering = ("-creado",)

    fieldsets = (
        ("Mensaje", {
            "fields": ("nombre", "email", "mensaje")
        }),
        ("Estado", {
            "fields": ("leido", "creado")
        }),
    )


# ======================================
# ⚙️ CONFIGURACIÓN DEL SITIO
# ======================================
@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        # 🔥 SOLO UNA CONFIG
        return not ConfiguracionSitio.objects.exists()

    fieldsets = (
        ("Información general", {
            "fields": ("nombre_sitio",)
        }),
        ("Contacto", {
            "fields": ("telefono", "email", "whatsapp")
        }),
        ("Redes sociales", {
            "fields": ("instagram", "facebook", "tiktok")
        }),
        ("Ubicación", {
            "fields": ("direccion", "mapa_embed")
        }),
    )


# ======================================
# 🧾 INSCRIPCIONES INLINE (🔥 PRO)
# ======================================
class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    readonly_fields = ("nombre", "email", "telefono", "mensaje", "creado")
    can_delete = False


# ======================================
# 🌱 TALLERES
# ======================================
@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):

    list_display = (
        "titulo",
        "fecha",
        "precio",
        "cupos",
        "activo",
        "destacado"
    )

    list_filter = ("activo", "destacado", "fecha")
    search_fields = ("titulo", "descripcion")

    list_editable = ("precio", "cupos", "activo", "destacado")

    prepopulated_fields = {"slug": ("titulo",)}

    ordering = ("-fecha",)

    inlines = [InscripcionInline]

    fieldsets = (
        ("Información principal", {
            "fields": ("titulo", "slug", "descripcion", "contenido")
        }),
        ("Imagen", {
            "fields": ("imagen",)
        }),
        ("Detalles del taller", {
            "fields": ("fecha", "duracion", "cupos", "precio")
        }),
        ("Configuración", {
            "fields": ("activo", "destacado")
        }),
    )


# ======================================
#  INSCRIPCIONES (VISTA DIRECTA)
# ======================================
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):

    list_display = ("nombre", "email", "taller", "creado")
    list_filter = ("taller", "creado")
    search_fields = ("nombre", "email")

    readonly_fields = ("creado",)

    ordering = ("-creado",)




@admin.register(PaginaLegal)
class PaginaLegalAdmin(admin.ModelAdmin):

    list_display = ("titulo", "tipo", "actualizado")
    list_filter = ("tipo",)
    search_fields = ("titulo", "contenido")

    def has_add_permission(self, request):
        # solo 1 por tipo
        if PaginaLegal.objects.count() >= 2:
            return False
        return True