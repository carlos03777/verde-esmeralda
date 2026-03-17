from django.db import models

# Create your models here.
from django.db import models


class PostCategory(models.Model):

    nombre = models.CharField(max_length=120)

    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre
    
class Post(models.Model):

    categoria = models.ForeignKey(PostCategory, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    imagen = models.ImageField(upload_to="blog")

    excerpt = models.CharField(max_length=200)

    contenido = models.TextField()

    publicado = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)

    actualizado = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.titulo
    
