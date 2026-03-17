# from allauth.account.signals import user_signed_up
# from django.dispatch import receiver
# from .models import Profile

# @receiver(user_signed_up)
# def create_profile_social(request, user, **kwargs):
#     # Solo crear el perfil cuando el usuario se haya registrado
#     if user:  # Asegura que haya un usuario válido
#         Profile.objects.get_or_create(usuario=user)