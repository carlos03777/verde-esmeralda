from django.urls import path
from . import views  #  ESTA LÍNEA FALTA

urlpatterns = [
    path("", views.home_view, name="home"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path("contacto/", views.contacto, name="contacto"),

    path("talleres/", views.talleres, name="talleres"),

    path("taller/<slug:slug>/", views.taller_detalle, name="taller_detalle"),

]