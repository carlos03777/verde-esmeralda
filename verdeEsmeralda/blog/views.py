from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F
from django.contrib import messages
from django.http import JsonResponse

from .models import Post, PostCategory, Comentario, Like


# ======================================
# LISTADO BLOG
# ======================================
def blog(request):

    posts = Post.objects.filter(publicado=True).select_related("categoria", "autor").order_by("-creado")

    categorias = PostCategory.objects.all()

    context = {
        "posts": posts,
        "categorias": categorias
    }

    return render(request, "blog/blog.html", context)


# ======================================
# DETALLE POST (🔥 COMPLETO)
# ======================================
def post_detalle(request, slug):

    post = get_object_or_404(
        Post.objects.select_related("categoria", "autor"),
        slug=slug,
        publicado=True
    )

    # 🔥 VISITAS
    Post.objects.filter(id=post.id).update(visitas=F("visitas") + 1)
    post.refresh_from_db()

    # ======================================
    # 🔥 COMENTARIOS
    # ======================================
    if request.method == "POST":

        contenido = request.POST.get("contenido")

        if not contenido:
            messages.warning(request, "El comentario no puede estar vacío")
            return redirect(post.get_absolute_url())

        if request.user.is_authenticated:

            Comentario.objects.create(
                post=post,
                usuario=request.user,
                contenido=contenido,
                aprobado=True
            )

        else:

            nombre = request.POST.get("nombre")
            email = request.POST.get("email")

            if not nombre or not email:
                messages.warning(request, "Debes completar nombre y email")
                return redirect(post.get_absolute_url())

            Comentario.objects.create(
                post=post,
                nombre=nombre,
                email=email,
                contenido=contenido,
                aprobado=True
            )

        messages.success(request, "Comentario enviado correctamente")
        return redirect(post.get_absolute_url())

    comentarios = post.comentarios.filter(aprobado=True).order_by("-creado")

    # ======================================
    # 🔥 RELACIONADOS
    # ======================================
    relacionados = Post.objects.filter(
        categoria=post.categoria,
        publicado=True
    ).exclude(id=post.id).order_by("-creado")[:4]

    # ======================================
    # 🔥 RECIENTES (FIX)
    # ======================================
    recientes = Post.objects.filter(
        publicado=True
    ).exclude(id=post.id).order_by("-creado")[:5]

    # ======================================
    # 🔥 CATEGORÍAS (FIX)
    # ======================================
    categorias = PostCategory.objects.all()

    # ======================================
    # 🔥 LIKES
    # ======================================
    user = request.user
    ip = get_client_ip(request)

    if user.is_authenticated:
        ya_dio_like = Like.objects.filter(post=post, usuario=user).exists()
    else:
        ya_dio_like = Like.objects.filter(post=post, ip=ip).exists()

    context = {
        "post": post,
        "comentarios": comentarios,
        "relacionados": relacionados,
        "recientes": recientes,      # 🔥 FIX
        "categorias": categorias,    # 🔥 FIX
        "likes_count": post.likes.count(),
        "ya_dio_like": ya_dio_like
    }

    return render(request, "blog/post_detalle.html", context)


# ======================================
# 🔥 LIKE
# ======================================
def like_post(request, slug):

    post = get_object_or_404(Post, slug=slug)

    user = request.user
    ip = get_client_ip(request)

    if user.is_authenticated:

        like, created = Like.objects.get_or_create(
            post=post,
            usuario=user
        )

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

    else:

        like, created = Like.objects.get_or_create(
            post=post,
            ip=ip
        )

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

    return JsonResponse({
        "liked": liked,
        "total": post.likes.count()
    })


# ======================================
# FILTRAR POR CATEGORÍA
# ======================================
def categoria_posts(request, slug):

    categoria = get_object_or_404(PostCategory, slug=slug)

    posts = Post.objects.filter(
        categoria=categoria,
        publicado=True
    ).order_by("-creado")

    categorias = PostCategory.objects.all()

    context = {
        "posts": posts,
        "categoria_actual": categoria,
        "categorias": categorias
    }

    return render(request, "blog/blog.html", context)


# ======================================
# BUSCADOR (🔥 CORREGIDO)
# ======================================
def buscar_posts(request):

    query = request.GET.get("q")
    categoria_slug = request.GET.get("categoria")

    posts = Post.objects.filter(publicado=True)

    if query:
        posts = posts.filter(titulo__icontains=query)

    if categoria_slug:
        posts = posts.filter(categoria__slug=categoria_slug)

    posts = posts.order_by("-creado")

    categorias = PostCategory.objects.all()

    context = {
        "posts": posts,
        "categorias": categorias,
        "query": query,
        "categoria_actual": PostCategory.objects.filter(slug=categoria_slug).first()
    }

    return render(request, "blog/blog.html", context)


# ======================================
# 🔥 HELPER IP
# ======================================
def get_client_ip(request):

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip