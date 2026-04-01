from django.shortcuts import render, get_object_or_404
from .models import Producto

def tienda(request):

    productos = Producto.objects.filter(disponible=True)

    # 🔍 BUSCADOR
    query = request.GET.get("q")
    if query:
        productos = productos.filter(nombre__icontains=query)

    # 🏷️ CATEGORIA
    categoria = request.GET.get("categoria")
    if categoria:
        productos = productos.filter(categoria__slug=categoria)

    return render(request, "productos/tienda.html", {
        "productos": productos
    })

def detalle_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug, disponible=True)

    relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        disponible=True
    ).exclude(id=producto.id)[:5]

    # 🔥 cantidad en sesión
    cantidad = request.session.get(f"cantidad_{producto.id}", 1)

    context = {
        "producto": producto,
        "imagenes": producto.imagenes.all(),
        "relacionados": relacionados,
        "cantidad": cantidad
    }

    return render(request, "productos/detalle_producto.html", context)