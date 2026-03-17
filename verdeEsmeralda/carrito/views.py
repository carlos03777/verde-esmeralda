from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto
from .models import Carrito, CarritoItem


# ======================================
# HELPER: OBTENER O CREAR CARRITO
# ======================================

def obtener_carrito(usuario):
    carrito, created = Carrito.objects.get_or_create(usuario=usuario)
    return carrito


# ======================================
# AGREGAR AL CARRITO
# ======================================

def agregar_al_carrito(request, producto_id):

    if not request.user.is_authenticated:
        return redirect("account_login")

    producto = get_object_or_404(Producto, id=producto_id)

    carrito = obtener_carrito(request.user)

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("ver_carrito")


# ======================================
# VER CARRITO
# ======================================

def ver_carrito(request):

    if not request.user.is_authenticated:
        return redirect("account_login")

    carrito = obtener_carrito(request.user)

    items = carrito.carritoitem_set.select_related("producto")

    total = sum(item.subtotal for item in items)

    context = {
        "items": items,
        "total": total
    }

    return render(request, "carrito/carrito.html", context)


# ======================================
# ELIMINAR PRODUCTO
# ======================================

def eliminar_del_carrito(request, producto_id):

    if not request.user.is_authenticated:
        return redirect("account_login")

    carrito = obtener_carrito(request.user)

    item = get_object_or_404(
        CarritoItem,
        carrito=carrito,
        producto_id=producto_id
    )

    item.delete()

    return redirect("ver_carrito")


# ======================================
# ACTUALIZAR CANTIDAD
# ======================================

def actualizar_cantidad(request, producto_id, accion):

    if not request.user.is_authenticated:
        return redirect("account_login")

    carrito = obtener_carrito(request.user)

    item = get_object_or_404(
        CarritoItem,
        carrito=carrito,
        producto_id=producto_id
    )

    if accion == "sumar":
        item.quantity += 1

    elif accion == "restar":
        item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
            return redirect("ver_carrito")

    item.save()

    return redirect("ver_carrito")


from django.views.decorators.http import require_POST

@require_POST
def vaciar_carrito(request):
    carrito = Carrito.objects.get(usuario=request.user)
    carrito.carritoitem_set.all().delete()
    return redirect("ver_carrito")