from django.db import models
from ordenes.models import Orden


class Pagos(models.Model):

    METODO = (
        ("stripe","Stripe"),
        ("paypal","Paypal"),
        ("mercadopago","MercadoPago"),
    )

    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)

    metodo = models.CharField(max_length=50, choices=METODO)

    transaccionId = models.CharField(max_length=200)

    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    estado = models.CharField(max_length=50)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaccionId
    

