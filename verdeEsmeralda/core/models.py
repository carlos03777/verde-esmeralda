
# Create your models here.
from django.db import models


class Nosotros(models.Model):

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    historia = models.TextField(blank=True)

    imagen = models.ImageField(upload_to="nosotros")

    frase = models.CharField(max_length=200, blank=True)

    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Equipo(models.Model):

    nombre = models.CharField(max_length=120)

    cargo = models.CharField(max_length=120)

    descripcion = models.TextField(blank=True)

    foto = models.ImageField(upload_to="equipo")

    activo = models.BooleanField(default=True)

    orden = models.PositiveIntegerField(default=0)

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"
    


class Contacto(models.Model):

    titulo = models.CharField(max_length=200, default="Contáctanos")
    descripcion = models.TextField(blank=True)

    email = models.EmailField()
    telefono = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    horario = models.CharField(max_length=200, blank=True)

    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class MensajeContacto(models.Model):

    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    mensaje = models.TextField()

    leido = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"
    


class ConfiguracionSitio(models.Model):

    nombre_sitio = models.CharField(max_length=150, default="Verde Esmeralda")

    # 📱 CONTACTO
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    #  REDES SOCIALES
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)

    #  UBICACIÓN
    direccion = models.CharField(max_length=255, blank=True)
    mapa_embed = models.TextField(blank=True)  # iframe de Google Maps

    def __str__(self):
        return "Configuración del sitio"
    




class Taller(models.Model):

    titulo = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    descripcion = models.TextField()

    contenido = models.TextField(blank=True)  # para detalle tipo blog

    imagen = models.ImageField(upload_to="talleres")

    fecha = models.DateTimeField()

    duracion = models.CharField(max_length=100, blank=True)

    cupos = models.PositiveIntegerField(default=10)

    precio = models.DecimalField(max_digits=10, decimal_places=2)

    activo = models.BooleanField(default=True)

    destacado = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("taller_detalle", args=[self.slug])

    def disponibles(self):
        inscritos = self.inscripciones.count()
        return self.cupos - inscritos


# ======================================
#  INSCRIPCIONES
# ======================================

class Inscripcion(models.Model):

    taller = models.ForeignKey(
        Taller,
        related_name="inscripciones",
        on_delete=models.CASCADE
    )

    nombre = models.CharField(max_length=120)

    email = models.EmailField()

    telefono = models.CharField(max_length=20, blank=True)

    mensaje = models.TextField(blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.taller.titulo}"