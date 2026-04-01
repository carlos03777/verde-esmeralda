from .models import ConfiguracionSitio

def config_sitio(request):
    return {
        "config": ConfiguracionSitio.objects.first()
    }