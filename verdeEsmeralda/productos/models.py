from django.db import models

# Create your models here.



class Categoria(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    descripcion = models.TextField()

    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    stock = models.IntegerField()

    disponible = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    @property
    def precio_final(self):
        if self.descuento:
            return self.precio - self.descuento
        return self.precio
    
class ImagenProducto(models.Model):

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")

    imagen = models.ImageField(upload_to="productos")

    def __str__(self):
        return self.producto.nombre