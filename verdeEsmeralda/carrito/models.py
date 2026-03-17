from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto


class Carrito(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito {self.id}"
    

class CarritoItem(models.Model):

    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.producto.nombre

    @property
    def subtotal(self):
        return self.producto.precio_final * self.quantity
    
    