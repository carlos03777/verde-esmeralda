from .models import Wishlist

def wishlist_contador(request):

    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.get(usuario=request.user)
            total = wishlist.wishlistitem_set.count()
        except Wishlist.DoesNotExist:
            total = 0
    else:
        total = 0

    return {
        "wishlist_total": total
    }