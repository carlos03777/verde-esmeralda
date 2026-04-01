from .models import Carrito


def carrito_contador(request):

    total_items = 0

    # ======================================
    # USUARIO AUTENTICADO → DB
    # ======================================
    if request.user.is_authenticated:

        try:
            carrito = Carrito.objects.get(usuario=request.user)
            total_items = sum(
                item.quantity for item in carrito.carritoitem_set.all()
            )
        except Carrito.DoesNotExist:
            total_items = 0

    # ======================================
    # USUARIO NO AUTENTICADO → SESSION
    # ======================================
    else:

        carrito = request.session.get("carrito", {})

        total_items = sum(carrito.values())

    return {
        "carrito_total": total_items
    }


# from .models import Carrito

# def carrito_contador(request):

#     if request.user.is_authenticated:
#         try:
#             carrito = Carrito.objects.get(usuario=request.user)
#             total_items = sum(item.quantity for item in carrito.carritoitem_set.all())
#         except Carrito.DoesNotExist:
#             total_items = 0
#     else:
#         total_items = 0

#     return {
#         "carrito_total": total_items
#     }