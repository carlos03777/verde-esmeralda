from django.shortcuts import render
from productos.models import Producto, Categoria
from blog.models import Post


def home_view(request):

    categorias = Categoria.objects.all()[:7]

    productos_destacados = Producto.objects.all()[:4]

    productos = Producto.objects.all()[:16]

    posts = Post.objects.filter(publicado=True)[:6]

    context = {
        "categorias": categorias,
        "productos_destacados": productos_destacados,
        "productos": productos,
        "posts": posts
    }

    return render(request, "core/home.html", context)