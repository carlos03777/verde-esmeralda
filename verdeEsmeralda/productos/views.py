from django.shortcuts import render
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