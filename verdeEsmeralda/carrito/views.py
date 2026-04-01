from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from productos.models import Producto
from .models import Carrito, CarritoItem


# ======================================
# HELPER: OBTENER O CREAR CARRITO (DB)
# ======================================

def obtener_carrito(usuario):
    carrito, created = Carrito.objects.get_or_create(usuario=usuario)
    return carrito


# ======================================
# HELPER: CARRITO EN SESSION
# ======================================

def obtener_carrito_session(request):
    return request.session.get("carrito", {})


def guardar_carrito_session(request, carrito):
    request.session["carrito"] = carrito
    request.session.modified = True


# ======================================
# AGREGAR AL CARRITO (MEJORADO 🔥)
# ======================================

@require_POST
def agregar_al_carrito(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    if producto.stock <= 0:
        messages.error(request, f"{producto.nombre} no tiene stock disponible")
        return redirect(request.META.get("HTTP_REFERER", "ver_carrito"))

    # 🔥 cantidad enviada desde el template
    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except ValueError:
        cantidad = 1

    if cantidad < 1:
        cantidad = 1

    # ======================================
    # USUARIO AUTENTICADO → DB
    # ======================================
    if request.user.is_authenticated:

        carrito = obtener_carrito(request.user)

        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto
        )

        if created:
            nueva_cantidad = min(cantidad, producto.stock)
            item.quantity = nueva_cantidad

            if cantidad > producto.stock:
                messages.warning(
                    request,
                    f"Solo hay {producto.stock} unidades disponibles"
                )
            else:
                messages.success(
                    request,
                    f"{producto.nombre} agregado al carrito ({nueva_cantidad})"
                )

        else:
            nueva_cantidad = item.quantity + cantidad

            if nueva_cantidad > producto.stock:
                item.quantity = producto.stock
                messages.warning(
                    request,
                    f"Stock máximo alcanzado ({producto.stock}) para {producto.nombre}"
                )
            else:
                item.quantity = nueva_cantidad
                messages.success(
                    request,
                    f"Se agregaron {cantidad} unidades de {producto.nombre}"
                )

        item.save()

    # ======================================
    # USUARIO NO AUTENTICADO → SESSION
    # ======================================
    else:

        carrito = obtener_carrito_session(request)
        producto_id_str = str(producto.id)

        cantidad_actual = carrito.get(producto_id_str, 0)
        nueva_cantidad = cantidad_actual + cantidad

        if nueva_cantidad > producto.stock:
            carrito[producto_id_str] = producto.stock
            messages.warning(
                request,
                f"Stock máximo alcanzado ({producto.stock}) para {producto.nombre}"
            )
        else:
            carrito[producto_id_str] = nueva_cantidad
            messages.success(
                request,
                f"Se agregaron {cantidad} unidades de {producto.nombre}"
            )

        guardar_carrito_session(request, carrito)

    return redirect(request.META.get("HTTP_REFERER", "ver_carrito"))


# ======================================
# VER CARRITO (HÍBRIDO)
# ======================================

def ver_carrito(request):

    items = []
    total = 0

    if request.user.is_authenticated:

        carrito = obtener_carrito(request.user)
        items = carrito.carritoitem_set.select_related("producto")
        total = sum(item.subtotal for item in items)

    else:

        carrito = obtener_carrito_session(request)

        for producto_id, cantidad in carrito.items():

            producto = get_object_or_404(Producto, id=producto_id)
            subtotal = producto.precio_final * cantidad

            items.append({
                "producto": producto,
                "quantity": cantidad,
                "subtotal": subtotal
            })

            total += subtotal

    context = {
        "items": items,
        "total": total
    }

    return render(request, "carrito/carrito.html", context)


# ======================================
# ELIMINAR PRODUCTO
# ======================================

def eliminar_del_carrito(request, producto_id):

    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:

        carrito = obtener_carrito(request.user)

        item = get_object_or_404(
            CarritoItem,
            carrito=carrito,
            producto=producto
        )

        item.delete()

    else:

        carrito = obtener_carrito_session(request)
        producto_id_str = str(producto_id)

        if producto_id_str in carrito:
            del carrito[producto_id_str]
            guardar_carrito_session(request, carrito)

    messages.success(request, f"{producto.nombre} eliminado del carrito")

    return redirect("ver_carrito")


# ======================================
# ACTUALIZAR CANTIDAD
# ======================================

def actualizar_cantidad(request, producto_id, accion):

    producto = get_object_or_404(Producto, id=producto_id)

    if request.user.is_authenticated:

        carrito = obtener_carrito(request.user)

        item = get_object_or_404(
            CarritoItem,
            carrito=carrito,
            producto=producto
        )

        if accion == "sumar":

            if item.quantity >= producto.stock:
                messages.warning(
                    request,
                    f"Stock máximo alcanzado ({producto.stock}) para {producto.nombre}"
                )
                return redirect("ver_carrito")

            item.quantity += 1
            item.save()

        elif accion == "restar":

            item.quantity -= 1

            if item.quantity <= 0:
                item.delete()
                messages.info(request, f"{producto.nombre} eliminado del carrito")
                return redirect("ver_carrito")

            item.save()

    else:

        carrito = obtener_carrito_session(request)
        producto_id_str = str(producto_id)

        if producto_id_str in carrito:

            if accion == "sumar":

                if carrito[producto_id_str] < producto.stock:
                    carrito[producto_id_str] += 1

            elif accion == "restar":

                carrito[producto_id_str] -= 1

                if carrito[producto_id_str] <= 0:
                    del carrito[producto_id_str]

            guardar_carrito_session(request, carrito)

    return redirect("ver_carrito")


# ======================================
# VACIAR CARRITO
# ======================================

@require_POST
def vaciar_carrito(request):

    if request.user.is_authenticated:

        carrito = obtener_carrito(request.user)

        if carrito.carritoitem_set.exists():
            carrito.carritoitem_set.all().delete()
            messages.success(request, "Carrito vaciado correctamente")
        else:
            messages.info(request, "El carrito ya está vacío")

    else:

        request.session["carrito"] = {}
        request.session.modified = True
        messages.success(request, "Carrito vaciado correctamente")

    return redirect("ver_carrito")