from django.contrib import admin
from .models import Wishlist


# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):

#     list_display = (
#         "usuario",
#         "producto",
#         "creado",
#     )

#     search_fields = (
#         "usuario__username",
#         "producto__nombre",
#     )

#     list_filter = ("creado",)