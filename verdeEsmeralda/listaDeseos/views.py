from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from productos.models import Producto
from .models import Wishlist, WishlistItem


@login_required
def ver_wishlist(request):

    wishlist, created = Wishlist.objects.get_or_create(usuario=request.user)

    items = wishlist.wishlistitem_set.select_related("producto")

    return render(request, "listaDeseos/wishlist.html", {
        "items": items
    })


@login_required
def agregar_a_wishlist(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    wishlist, created = Wishlist.objects.get_or_create(usuario=request.user)

    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        producto=producto
    )

    return redirect(request.META.get("HTTP_REFERER", "ver_wishlist"))


@login_required
def eliminar_de_wishlist(request, producto_id):

    wishlist = get_object_or_404(Wishlist, usuario=request.user)

    item = WishlistItem.objects.filter(
        wishlist=wishlist,
        producto_id=producto_id
    ).first()

    if item:
        item.delete()

    return redirect("ver_wishlist")

from django.shortcuts import redirect, get_object_or_404
from productos.models import Producto
from .models import Wishlist
from carrito.models import CarritoItem

def mover_a_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Agregar al carrito
    item, created = CarritoItem.objects.get_or_create(
        usuario=request.user,
        producto=producto
    )

    if not created:
        item.quantity += 1
        item.save()

    # Eliminar de wishlist
    Wishlist.objects.filter(usuario=request.user, producto=producto).delete()

    return redirect("ver_wishlist")