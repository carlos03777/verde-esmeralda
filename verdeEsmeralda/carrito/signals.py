from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from productos.models import Producto
from .models import Carrito, CarritoItem


@receiver(user_logged_in)
def fusionar_carrito_al_login(sender, request, user, **kwargs):

    carrito_session = request.session.get("carrito", {})

    if not carrito_session:
        return  # no hay nada que fusionar

    carrito_db, _ = Carrito.objects.get_or_create(usuario=user)

    for producto_id, cantidad_session in carrito_session.items():

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            continue

        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito_db,
            producto=producto
        )

        if created:
            # 👉 si es nuevo, limitar por stock
            item.quantity = min(cantidad_session, producto.stock)

        else:
            # 👉 si ya existía, sumar pero respetar stock
            nueva_cantidad = item.quantity + cantidad_session
            item.quantity = min(nueva_cantidad, producto.stock)

        item.save()

    # 🧹 limpiar carrito de session
    request.session["carrito"] = {}
    request.session.modified = True