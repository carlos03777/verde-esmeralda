from django.urls import path
from . import views

urlpatterns = [
    path("pagar/<int:orden_id>/", views.iniciar_pago, name="iniciar_pago"),
    path("retorno/", views.retorno_pago, name="retorno_pago"),
    path("resultado/<int:pago_id>/", views.resultado_pago, name="resultado_pago"),

    # 🔥 NUEVO: WEBHOOK WOMPI
    path("webhook/", views.webhook_wompi, name="webhook_wompi"),
    
]