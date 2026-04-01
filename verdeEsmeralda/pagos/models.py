from django.db import models
from django.contrib.auth.models import User
from ordenes.models import Orden


class Pago(models.Model):

    ESTADO = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("declined", "Declined"),
        ("error", "Error"),
    )

    METODO = (
        ("card", "Tarjeta"),
        ("pse", "PSE"),
        ("nequi", "Nequi"),
        ("daviplata", "Daviplata"),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)

    monto = models.DecimalField(max_digits=10, decimal_places=2)

    estado = models.CharField(max_length=20, choices=ESTADO, default="pending")

    metodo_pago = models.CharField(
        max_length=20,
        choices=METODO,
        null=True,
        blank=True
    )

    referencia = models.CharField(
        max_length=200,
        unique=True
    )  # referencia interna

    wompi_id = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )  # id de la transacción en Wompi

    respuesta = models.JSONField(
        null=True,
        blank=True
    )  # guardar respuesta completa del gateway (PRO)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pago {self.id} - {self.estado}"