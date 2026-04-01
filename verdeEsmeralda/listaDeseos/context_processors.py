from .models import Wishlist

def wishlist_contador(request):

    productos_ids = set()

    # SESSION
    wishlist_session = request.session.get("wishlist", [])
    productos_ids.update(wishlist_session)

    # DB
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(usuario=request.user)
            db_ids = wishlist.wishlistitem_set.values_list("producto_id", flat=True)
            productos_ids.update(map(str, db_ids))
        except Wishlist.DoesNotExist:
            pass

    return {
        "wishlist_total": len(productos_ids)
    }