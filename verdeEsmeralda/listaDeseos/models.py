from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto


class Wishlist(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist de {self.usuario}"


class WishlistItem(models.Model):

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("wishlist", "producto")

    def __str__(self):
        return self.producto.nombre