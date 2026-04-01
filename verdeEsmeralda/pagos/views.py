import uuid
import hashlib
import requests
import json
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ordenes.models import Orden
from carrito.models import Carrito
from .models import Pago


# ======================================
# INICIAR PAGO
# ======================================
@login_required
def iniciar_pago(request, orden_id):

    orden = get_object_or_404(Orden, id=orden_id, user=request.user)

    if orden.estado == "paid":
        messages.info(request, "Esta orden ya fue pagada")
        return redirect("perfil")

    # 🔒 evitar múltiples órdenes pendientes
    orden_pendiente = Orden.objects.filter(
        user=request.user,
        estado="pending"
    ).order_by("-creado").first()

    if orden_pendiente and orden_pendiente.id != orden.id:
        return redirect("iniciar_pago", orden_id=orden_pendiente.id)

    # 🔁 reutilizar pago
    pago = Pago.objects.filter(orden=orden).first()

    if not pago:
        pago = Pago.objects.create(
            usuario=request.user,
            orden=orden,
            monto=orden.total,
            referencia=f"ORDEN-{orden.id}-{uuid.uuid4().hex[:8]}"
        )
    elif pago.estado in ["declined", "error"]:
        pago.referencia = f"ORDEN-{orden.id}-{uuid.uuid4().hex[:8]}"
        pago.estado = "pending"
        pago.save()

    referencia = pago.referencia
    monto = Decimal(pago.monto)
    amount_in_cents = int(monto * 100)


    cadena = f"{referencia}{amount_in_cents}COP{settings.WOMPI_INTEGRITY_KEY}"
    firma = hashlib.sha256(cadena.encode("utf-8")).hexdigest()

    context = {
        "public_key": settings.WOMPI_PUBLIC_KEY,
        "amount_in_cents": amount_in_cents,
        "reference": referencia,
        "signature": firma,
        "redirect_url": "https://unstridulating-cloddily-adalberto.ngrok-free.dev/pagos/retorno/"
    }

    return render(request, "pagos/wompi_checkout.html", context)

# ======================================
# RETORNO WOMPI (SOLO UX)
# ======================================
def retorno_pago(request):

    transaction_id = request.GET.get("id")

    if not transaction_id:
        messages.error(request, "Transacción no encontrada")
        return redirect("home")

    url = f"https://sandbox.wompi.co/v1/transactions/{transaction_id}"

    headers = {
        "Authorization": f"Bearer {settings.WOMPI_PRIVATE_KEY}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
    except Exception:
        messages.error(request, "Error conectando con Wompi")
        return redirect("home")

    if "data" not in data:
        messages.error(request, "Respuesta inválida de Wompi")
        return redirect("home")

    transaccion = data["data"]
    referencia = transaccion.get("reference")

    try:
        pago = Pago.objects.get(referencia=referencia)
    except Pago.DoesNotExist:
        messages.error(request, "Pago no encontrado")
        return redirect("home")

    return redirect("resultado_pago", pago_id=pago.id)


# ======================================
# WEBHOOK WOMPI (SEGURIDAD + PROCESAMIENTO)
# ======================================
@csrf_exempt
def webhook_wompi(request):

    print("\n======= WEBHOOK DEBUG =======")
    print("HEADERS:", request.headers)
    print("BODY:", request.body)
    print("=============================\n")

    if request.method != "POST":
        return HttpResponse(status=405)

    # ==============================
    # PARSE JSON
    # ==============================
    try:
        payload = json.loads(request.body)
    except Exception as e:
        print("ERROR JSON:", e)
        return HttpResponse(status=400)

    # ==============================
    # 🔐 VALIDACIÓN CHECKSUM WOMPI
    # ==============================
    checksum_header = request.headers.get("X-Event-Checksum")
    checksum_body = payload.get("signature", {}).get("checksum")

    if not checksum_header or checksum_header != checksum_body:
        print("❌ CHECKSUM INVALIDO")
        return HttpResponse(status=403)

    print("✅ CHECKSUM VALIDO")

    # ==============================
    # DATOS TRANSACCIÓN
    # ==============================
    data = payload.get("data", {})
    transaction = data.get("transaction", {})

    referencia = transaction.get("reference")
    estado = transaction.get("status")
    monto = transaction.get("amount_in_cents")
    moneda = transaction.get("currency")
    transaction_id = transaction.get("id")

    print("REF:", referencia)
    print("ESTADO:", estado)

    if not referencia:
        return HttpResponse(status=400)

    # ==============================
    # BUSCAR PAGO
    # ==============================
    try:
        pago = Pago.objects.select_related("orden").get(referencia=referencia)
    except Pago.DoesNotExist:
        print("PAGO NO ENCONTRADO")
        return HttpResponse(status=404)

    # evitar reprocesar
    if pago.estado == "approved":
        print("⚠️ YA PROCESADO")
        return HttpResponse(status=200)

    orden = pago.orden

    # ==============================
    # VALIDAR MONTO
    # ==============================
    monto_local = int(pago.monto * 100)

    if monto != monto_local or moneda != "COP":
        print("❌ ERROR MONTO")
        pago.estado = "declined"
        pago.save()
        return HttpResponse(status=200)

    # ==============================
    # PROCESAR ESTADO
    # ==============================
    if estado == "APPROVED":

        print("✅ PAGO APROBADO")

        pago.estado = "approved"
        pago.wompi_id = transaction_id
        pago.respuesta = payload
        pago.save()

        orden.estado = "paid"
        orden.save()

        # limpiar carrito
        Carrito.objects.filter(usuario=pago.usuario).delete()

        # descontar stock
        for item in orden.ordenitem_set.all():
            producto = item.producto
            producto.stock -= item.quantity
            producto.save()

    elif estado == "DECLINED":

        print("❌ PAGO RECHAZADO")

        pago.estado = "declined"
        pago.respuesta = payload
        pago.save()

        orden.estado = "pending"
        orden.save()

    else:
        print("⏳ PAGO PENDING")

        pago.estado = "pending"
        pago.respuesta = payload
        pago.save()

    return HttpResponse(status=200)


# ======================================
# RESULTADO
# ======================================
def resultado_pago(request, pago_id):

    pago = get_object_or_404(Pago, id=pago_id)

    return render(request, "pagos/resultado.html", {
        "pago": pago,
        "transaccion": pago.respuesta.get("data", {}) if pago.respuesta else {}
    })