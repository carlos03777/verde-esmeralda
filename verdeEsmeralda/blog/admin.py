from django.contrib import admin
from .models import Post, PostCategory, Comentario
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


# ======================================
# FORM CKEDITOR
# ======================================

class PostAdminForm(forms.ModelForm):
    contenido = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = "__all__"


# ======================================
# ADMIN POST
# ======================================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    list_display = ("titulo", "categoria", "publicado", "creado")
    list_filter = ("publicado", "categoria", "creado")
    search_fields = ("titulo", "contenido")

    prepopulated_fields = {"slug": ("titulo",)}

    ordering = ("-creado",)


# ======================================
# ADMIN CATEGORÍAS 🔥
# ======================================

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)

    prepopulated_fields = {"slug": ("nombre",)}


# ======================================
# ADMIN COMENTARIOS (PRO)
# ======================================

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("post", "usuario", "aprobado", "creado")
    list_filter = ("aprobado", "creado")
    search_fields = ("contenido",)

    actions = ["aprobar_comentarios"]

    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)