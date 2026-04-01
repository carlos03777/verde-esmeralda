from django.urls import path
from . import views

urlpatterns = [

    path("checkout/", views.checkout, name="checkout"),
    path("crear-orden/", views.crear_orden, name="crear_orden"),
    # path("agregar-direccion/", views.agregar_direccion_checkout, name="agregar_direccion_checkout",
        # DIRECCIONES
    path("direccion/nueva/", views.crear_direccion, name="crear_direccion"),
    path("direccion/<int:id>/editar/", views.editar_direccion, name="editar_direccion"),
    path("direccion/<int:id>/eliminar/", views.eliminar_direccion, name="eliminar_direccion"),


]