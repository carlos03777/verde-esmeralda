from django.urls import path
from . import views

urlpatterns = [
    path("", views.ver_wishlist, name="ver_wishlist"),
    path("agregar/<int:producto_id>/", views.agregar_a_wishlist, name="agregar_a_wishlist"),
    path("eliminar/<int:producto_id>/", views.eliminar_de_wishlist, name="eliminar_de_wishlist"),
]