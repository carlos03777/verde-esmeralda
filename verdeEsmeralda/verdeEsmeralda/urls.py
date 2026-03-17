
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #url de las apps
    path("", include("core.urls")),
    path("accounts/", include("allauth.urls")),
    path('productos/', include('productos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('carrito/', include('carrito.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('blog/', include('blog.urls')),
    path('pagos/', include('pagos.urls')),
    path('listaDeseos/', include('listaDeseos.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
