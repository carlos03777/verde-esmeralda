from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from .models import Profile
from ordenes.models import Orden, Direccion
from ordenes.forms import DireccionForm


@login_required
def profile_view(request):

    user = request.user
    profile = user.profile

    tab = request.GET.get("tab", "perfil")
    next_url = request.GET.get("next") or request.POST.get("next")

    ordenes = Orden.objects.filter(user=user).order_by("-creado")
    direcciones = Direccion.objects.filter(usuario=user)

    direccion_form = DireccionForm()
    direccion_edit = None

    # ======================================
    # EDITAR DIRECCION
    # ======================================

    edit_id = request.GET.get("editar")

    if edit_id:
        direccion_edit = get_object_or_404(
            Direccion,
            id=edit_id,
            usuario=user
        )
        direccion_form = DireccionForm(instance=direccion_edit)

    # ======================================
    # POST
    # ======================================

    if request.method == "POST":

        # ======================================
        # ACTUALIZAR PERFIL
        # ======================================

        if "update_profile" in request.POST:

            user.first_name = request.POST.get("first_name", "")
            user.last_name = request.POST.get("last_name", "")
            user.save()

            profile.celular = request.POST.get("phone", "")

            if request.FILES.get("avatar"):
                profile.avatar = request.FILES["avatar"]

            profile.save()

            messages.success(request, "Perfil actualizado")

            return redirect(reverse("perfil") + "?tab=perfil")

        # ======================================
        # GUARDAR DIRECCION
        # ======================================

        if "save_address" in request.POST:

            if direccion_edit:
                direccion_form = DireccionForm(
                    request.POST,
                    instance=direccion_edit
                )
            else:
                direccion_form = DireccionForm(request.POST)

            if direccion_form.is_valid():

                direccion = direccion_form.save(commit=False)
                direccion.usuario = user
                direccion.save()

                messages.success(request, "Dirección guardada")

                # Si viene desde checkout, volver al checkout
                if next_url:
                    return redirect(next_url)

                return redirect(reverse("perfil") + "?tab=direcciones")

        # ======================================
        # ELIMINAR DIRECCION
        # ======================================

        if "delete_address" in request.POST:

            direccion_id = request.POST.get("direccion_id")

            direccion = get_object_or_404(
                Direccion,
                id=direccion_id,
                usuario=user
            )

            direccion.delete()

            messages.success(request, "Dirección eliminada")

            return redirect(reverse("perfil") + "?tab=direcciones")

    # ======================================
    # CONTEXT
    # ======================================

    context = {
        "profile": profile,
        "ordenes": ordenes,
        "direcciones": direcciones,
        "direccion_form": direccion_form,
        "direccion_edit": direccion_edit,
        "tab": tab,
        "next_url": next_url,
    }

    return render(request, "usuarios/perfil.html", context)