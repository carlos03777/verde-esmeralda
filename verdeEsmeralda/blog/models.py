from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


# ======================================
# CATEGORÍAS
# ======================================

class PostCategory(models.Model):

    nombre = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ======================================
# POSTS
# ======================================

class Post(models.Model):

    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    categoria = models.ForeignKey(
        PostCategory,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    imagen = models.ImageField(upload_to="blog")

    excerpt = models.CharField(max_length=200)

    contenido = RichTextUploadingField()

    # ======================================
    # SEO
    # ======================================
    meta_title = models.CharField(max_length=60, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)

    # ======================================
    # CONTROL
    # ======================================
    publicado = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)

    # ======================================
    # MÉTRICAS
    # ======================================
    visitas = models.PositiveIntegerField(default=0)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("post_detalle", args=[self.slug])


# ======================================
# COMENTARIOS (🔥 MIXTO)
# ======================================

class Comentario(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )

    # 🔥 Usuario (opcional)
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comentarios"
    )

    # 🔥 Para anónimos
    nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    contenido = models.TextField()

    aprobado = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"

    def __str__(self):
        if self.usuario:
            return f"Comentario de {self.usuario.username}"
        return f"Comentario de {self.nombre}"


# ======================================
# LIKES (ANTI DUPLICADOS)
# ======================================

class Like(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    # 🔥 si está logueado
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # 🔥 fallback para anónimos
    ip = models.GenericIPAddressField(null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "usuario"],
                name="unique_like_user",
                condition=models.Q(usuario__isnull=False)
            ),
            models.UniqueConstraint(
                fields=["post", "ip"],
                name="unique_like_ip",
                condition=models.Q(usuario__isnull=True)
            ),
        ]
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return f"Like en {self.post.titulo}"