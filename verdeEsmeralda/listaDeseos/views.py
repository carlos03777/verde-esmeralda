from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from productos.models import Producto
from .models import Wishlist, WishlistItem
from carrito.models import CarritoItem
from carrito.views import obtener_carrito


# ======================================
# HELPERS SESSION
# ======================================

def obtener_wishlist_session(request):
    return request.session.get("wishlist", [])


def guardar_wishlist_session(request, wishlist):
    request.session["wishlist"] = wishlist
    request.session.modified = True


# ======================================
# 🔥 FUSIONAR SESSION → DB (CLAVE)
# ======================================

def fusionar_wishlist(request):

    if not request.user.is_authenticated:
        return

    wishlist_session = obtener_wishlist_session(request)

    if not wishlist_session:
        return

    wishlist_db, _ = Wishlist.objects.get_or_create(usuario=request.user)

    for producto_id in wishlist_session:

        producto = Producto.objects.filter(id=producto_id).first()

        if producto:
            WishlistItem.objects.get_or_create(
                wishlist=wishlist_db,
                producto=producto
            )

    # 🔥 limpiar session después de fusionar
    request.session["wishlist"] = []
    request.session.modified = True


# ======================================
# 🔥 CONTADOR GLOBAL (para navbar)
# ======================================

def contar_wishlist(request):

    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(usuario=request.user)
        return wishlist.wishlistitem_set.count()

    else:
        return len(obtener_wishlist_session(request))


# ======================================
# VER WISHLIST (HÍBRIDO + FUSIÓN)
# ======================================

def ver_wishlist(request):

    # 🔥 fusionar si aplica
    fusionar_wishlist(request)

    items = []

    if request.user.is_authenticated:

        wishlist, _ = Wishlist.objects.get_or_create(usuario=request.user)
        items = wishlist.wishlistitem_set.select_related("producto")

    else:

        wishlist = obtener_wishlist_session(request)

        for producto_id in wishlist:
            producto = get_object_or_404(Producto, id=producto_id)
            items.append({
                "producto": producto
            })

    return render(request, "listaDeseos/wishlist.html", {
        "items": items,
        "wishlist_count": contar_wishlist(request)  # 🔥 importante
    })


# ======================================
# AGREGAR A WISHLIST
# ======================================

def agregar_a_wishlist(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:

        wishlist, _ = Wishlist.objects.get_or_create(usuario=request.user)

        item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            producto=producto
        )

        if created:
            messages.success(request, f"{producto.nombre} agregado a favoritos")
        else:
            messages.info(request, f"{producto.nombre} ya está en favoritos")

    else:

        wishlist = obtener_wishlist_session(request)
        producto_id_str = str(producto.id)

        if producto_id_str not in wishlist:
            wishlist.append(producto_id_str)
            guardar_wishlist_session(request, wishlist)
            messages.success(request, f"{producto.nombre} agregado a favoritos")
        else:
            messages.info(request, f"{producto.nombre} ya está en favoritos")

    next_url = request.GET.get("next")
    return redirect(request.META.get("HTTP_REFERER", "ver_wishlist"))


# ======================================
# ELIMINAR DE WISHLIST
# ======================================

def eliminar_de_wishlist(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:

        wishlist = Wishlist.objects.filter(usuario=request.user).first()

        if wishlist:
            WishlistItem.objects.filter(
                wishlist=wishlist,
                producto=producto
            ).delete()

    else:

        wishlist = obtener_wishlist_session(request)
        producto_id_str = str(producto.id)

        if producto_id_str in wishlist:
            wishlist.remove(producto_id_str)
            guardar_wishlist_session(request, wishlist)

    messages.success(request, f"{producto.nombre} eliminado de favoritos")

    return redirect("ver_wishlist")


# ======================================
# MOVER A CARRITO
# ======================================

def mover_a_carrito(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:

        carrito = obtener_carrito(request.user)

        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto
        )

        if not created:
            if item.quantity < producto.stock:
                item.quantity += 1
                item.save()
            else:
                messages.warning(request, f"Stock máximo alcanzado para {producto.nombre}")

        wishlist = Wishlist.objects.filter(usuario=request.user).first()

        if wishlist:
            WishlistItem.objects.filter(
                wishlist=wishlist,
                producto=producto
            ).delete()

    else:

        carrito = request.session.get("carrito", {})
        producto_id_str = str(producto.id)

        cantidad_actual = carrito.get(producto_id_str, 0)

        if cantidad_actual < producto.stock:
            carrito[producto_id_str] = cantidad_actual + 1
            request.session["carrito"] = carrito
            request.session.modified = True
        else:
            messages.warning(request, f"Stock máximo alcanzado para {producto.nombre}")

        wishlist = obtener_wishlist_session(request)

        if producto_id_str in wishlist:
            wishlist.remove(producto_id_str)
            guardar_wishlist_session(request, wishlist)

    messages.success(request, f"{producto.nombre} movido al carrito")

    return redirect("ver_wishlist")