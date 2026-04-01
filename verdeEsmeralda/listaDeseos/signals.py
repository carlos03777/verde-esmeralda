from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Wishlist, WishlistItem
from productos.models import Producto


@receiver(user_logged_in)
def fusionar_wishlist_al_login(sender, request, user, **kwargs):

    wishlist_session = request.session.get("wishlist", [])

    if not wishlist_session:
        return  # no hay nada que fusionar

    # obtener o crear wishlist del usuario
    wishlist, created = Wishlist.objects.get_or_create(usuario=user)

    # productos que ya existen en DB
    existentes = set(
        wishlist.wishlistitem_set.values_list("producto_id", flat=True)
    )

    for producto_id in wishlist_session:

        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            continue

        if int(producto_id) not in existentes:
            WishlistItem.objects.create(
                wishlist=wishlist,
                producto=producto
            )

    # limpiar session después de fusionar
    request.session["wishlist"] = []
    request.session.modified = True