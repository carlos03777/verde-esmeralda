from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # datos personales
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)

    # contacto
    celular = models.CharField(max_length=20, blank=True)

    # direccion de envio
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=20, blank=True)

    # perfil
    avatar = models.ImageField(upload_to="usuarios", blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(usuario=instance)
    else:
        if hasattr(instance, "profile"):
            instance.profile.save()