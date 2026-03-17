from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto



class Direccion(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=200)

    celular = models.CharField(max_length=20)

    direccion = models.CharField(max_length=250)

    ciudad = models.CharField(max_length=100)

    departamento = models.CharField(max_length=100)

    codigoPostal = models.CharField(max_length=20)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.direccion
    
class Orden(models.Model):

    ESTADO = (
        ("pending","Pending"),
        ("paid","Paid"),
        ("shipped","Shipped"),
        ("completed","Completed"),
        ("cancelled","Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)

    total = models.DecimalField(max_digits=10, decimal_places=2)

    estado = models.CharField(max_length=20, choices=ESTADO, default="pending")

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id}"
    
class OrdenItem(models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.IntegerField()

    def __str__(self):
        return self.producto.nombre
    

class Seguimiento(models.Model):

    ESTADO = (
        ("preparing","Preparing"),
        ("shipped","Shipped"),
        ("in_transit","In transit"),
        ("delivered","Delivered"),
    )

    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)

    transportadora = models.CharField(max_length=100)

    numeroSeguimiento = models.CharField(max_length=200)

    estado = models.CharField(max_length=50, choices=ESTADO)

    fechaEnvio = models.DateTimeField(null=True, blank=True)

    fechaEntrega = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.numeroSeguimiento