from django.shortcuts import render, redirect, get_object_or_404

# 📦 Apps
from productos.models import Producto, Categoria
from blog.models import Post
from .models import Nosotros, Equipo, Contacto, MensajeContacto, Taller, Inscripcion

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactoForm

# ======================================
#  HOME
# ======================================
def home_view(request):

    categorias = Categoria.objects.all()[:7]

    productos_destacados = Producto.objects.all()[:4]

    productos = Producto.objects.all()[:16]

    posts = Post.objects.filter(publicado=True).order_by("-creado")[:6]

    context = {
        "categorias": categorias,
        "productos_destacados": productos_destacados,
        "productos": productos,
        "posts": posts,
    }

    return render(request, "core/home.html", context)


# ======================================
#  NOSOTROS
# ======================================
def nosotros(request):

    #  contenido principal (solo uno)
    data = Nosotros.objects.first()

    #  equipo dinámico
    equipo = Equipo.objects.filter(activo=True)

    context = {
        "data": data,
        "equipo": equipo,
    }

    return render(request, "core/nosotros.html", context)




# ======================================
# 📩 CONTACTO (🔥 PRO)
# ======================================

def contacto(request):

    info = Contacto.objects.first()

    form = ContactoForm()

    if request.method == "POST":

        form = ContactoForm(request.POST)

        if form.is_valid():

            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            mensaje = form.cleaned_data["mensaje"]

            # 💾 Guardar en BD
            MensajeContacto.objects.create(
                nombre=nombre,
                email=email,
                mensaje=mensaje
            )

            # ======================================
            # 📧 EMAIL AL ADMIN
            # ======================================
            try:
                send_mail(
                    subject=f" Nuevo mensaje de {nombre}",
                    message=f"""
Has recibido un nuevo mensaje:

Nombre: {nombre}
Email: {email}

Mensaje:
{mensaje}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception as e:
                print("Error enviando email admin:", e)

            # ======================================
            # 📧 AUTO-RESPUESTA AL USUARIO
            # ======================================
            try:
                send_mail(
                    subject="Hemos recibido tu mensaje ",
                    message=f"""
Hola {nombre},

Gracias por escribirnos en Verde Esmeralda 🌱

Hemos recibido tu mensaje y te responderemos lo más pronto posible.

Un abrazo natural 💚
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                print("Error enviando auto-respuesta:", e)

            messages.success(request, "Mensaje enviado correctamente ")

            return redirect("contacto")

        else:
            messages.warning(request, "Por favor corrige los errores del formulario")

    context = {
        "info": info,
        "form": form
    }

    return render(request, "core/contacto.html", context)





def talleres(request):

    talleres = Taller.objects.filter(activo=True).order_by("fecha")

    return render(request, "core/talleres.html", {
        "talleres": talleres
    })



def taller_detalle(request, slug):

    taller = get_object_or_404(Taller, slug=slug, activo=True)

    if request.method == "POST":

        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        mensaje = request.POST.get("mensaje")

        if not nombre or not email:
            messages.warning(request, "Nombre y email son obligatorios")
            return redirect(taller.get_absolute_url())

        # 🔥 guardar inscripción
        Inscripcion.objects.create(
            taller=taller,
            nombre=nombre,
            email=email,
            telefono=telefono,
            mensaje=mensaje
        )

        messages.success(request, "Te has inscrito correctamente ")
        return redirect(taller.get_absolute_url())

    return render(request, "core/taller_detalle.html", {
        "taller": taller
    })