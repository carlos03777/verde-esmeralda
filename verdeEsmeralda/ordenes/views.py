from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from productos.models import Producto
from carrito.models import Carrito
from .models import Orden, OrdenItem, Direccion
from .forms import DireccionForm


# ======================================
# CHECKOUT
# ======================================

@login_required
def checkout(request):

    carrito = get_object_or_404(Carrito, usuario=request.user)
    items_carrito = carrito.carritoitem_set.select_related("producto")

    if not items_carrito.exists():
        messages.warning(request, "Tu carrito está vacío")
        return redirect("ver_carrito")

    items = []
    total = 0

    for item in items_carrito:
        subtotal = item.subtotal
        total += subtotal

        items.append({
            "producto": item.producto,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    direcciones = Direccion.objects.filter(usuario=request.user)

    context = {
        "items": items,
        "total": total,
        "direcciones": direcciones
    }

    return render(request, "ordenes/checkout.html", context)


# ======================================
# CREAR / REUTILIZAR ORDEN
# ======================================

@login_required
def crear_orden(request):

    if request.method != "POST":
        return redirect("checkout")

    carrito = get_object_or_404(Carrito, usuario=request.user)
    items_carrito = carrito.carritoitem_set.select_related("producto")

    if not items_carrito.exists():
        messages.error(request, "Tu carrito está vacío")
        return redirect("ver_carrito")

    direccion_id = request.POST.get("direccion")

    if not direccion_id:
        messages.error(request, "Debes seleccionar una dirección")
        return redirect("checkout")

    direccion = get_object_or_404(
        Direccion,
        id=direccion_id,
        usuario=request.user
    )

    total = 0

    with transaction.atomic():

        # 🔒 bloquear productos
        productos_ids = [item.producto.id for item in items_carrito]

        productos = Producto.objects.select_for_update().filter(
            id__in=productos_ids
        )

        productos_dict = {p.id: p for p in productos}

        # ======================================
        # VALIDAR STOCK
        # ======================================
        for item in items_carrito:

            producto = productos_dict.get(item.producto.id)

            if not producto:
                messages.error(request, "Producto no encontrado")
                return redirect("ver_carrito")

            if producto.stock < item.quantity:
                messages.error(
                    request,
                    f"No hay suficiente stock de {producto.nombre}"
                )
                return redirect("ver_carrito")

            total += item.subtotal

        # ======================================
        # 🔥 REUTILIZAR ORDEN PENDIENTE
        # ======================================
        orden = Orden.objects.filter(
            user=request.user,
            estado="pending"
        ).first()

        if orden:
            # 👉 actualizar dirección y total
            orden.direccion = direccion
            orden.total = total
            orden.save()

            # 👉 eliminar items anteriores
            orden.ordenitem_set.all().delete()

        else:
            # 👉 crear nueva
            orden = Orden.objects.create(
                user=request.user,
                direccion=direccion,
                total=total,
                estado="pending"
            )

        # ======================================
        # CREAR ITEMS NUEVOS
        # ======================================
        items_orden = []

        for item in items_carrito:

            producto = productos_dict.get(item.producto.id)

            items_orden.append(
                OrdenItem(
                    orden=orden,
                    producto=producto,
                    price=producto.precio,
                    quantity=item.quantity
                )
            )

        OrdenItem.objects.bulk_create(items_orden)

        # ❗ NO vaciar carrito aún
        # ❗ NO descontar stock aquí

    messages.success(request, "Orden lista. Procede al pago.")

    return redirect("iniciar_pago", orden_id=orden.id)


# ======================================
# DIRECCIONES
# ======================================

@login_required
def crear_direccion(request):

    if request.method == "POST":
        form = DireccionForm(request.POST)

        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.usuario = request.user
            direccion.save()

            messages.success(request, "Dirección agregada correctamente")
            return redirect(reverse("perfil") + "?tab=direcciones")

    else:
        form = DireccionForm()

    return render(request, "ordenes/direccion_form.html", {"form": form})


@login_required
def editar_direccion(request, id):

    direccion = get_object_or_404(
        Direccion,
        id=id,
        usuario=request.user
    )

    if request.method == "POST":
        form = DireccionForm(request.POST, instance=direccion)

        if form.is_valid():
            form.save()
            messages.success(request, "Dirección actualizada")
            return redirect(reverse("perfil") + "?tab=direcciones")

    else:
        form = DireccionForm(instance=direccion)

    return render(request, "ordenes/direccion_form.html", {"form": form})


@login_required
def eliminar_direccion(request, id):

    direccion = get_object_or_404(
        Direccion,
        id=id,
        usuario=request.user
    )

    if request.method == "POST":
        direccion.delete()
        messages.success(request, "Dirección eliminada")

    return redirect(reverse("perfil") + "?tab=direcciones")