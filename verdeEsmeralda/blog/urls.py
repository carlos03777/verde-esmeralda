from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog, name="blog"),
    path("buscar/", views.buscar_posts, name="buscar_posts"),
    path("categoria/<slug:slug>/", views.categoria_posts, name="categoria_posts"),
    path("like/<slug:slug>/", views.like_post, name="like_post"),
    path("<slug:slug>/", views.post_detalle, name="post_detalle"),
]