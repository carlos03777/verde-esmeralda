from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("usuario", "celular", "ciudad", "creado")

    list_filter = ("ciudad", "creado")

    search_fields = (
        "usuario__username",
        "usuario__email",
        "celular",
    )

    ordering = ("-creado",)

    readonly_fields = ("creado",)