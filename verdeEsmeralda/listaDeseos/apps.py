from django.apps import AppConfig

class WishlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listaDeseos'

    def ready(self):
        import listaDeseos.signals