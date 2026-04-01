from django.urls import path
from . import views

urlpatterns = [
    path("", views.tienda, name="tienda"),
    path("producto/<slug:slug>/", views.detalle_producto, name="detalle_producto"),

]