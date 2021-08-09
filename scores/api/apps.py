from django.apps import AppConfig
from .bus import Bus


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # avoiding importing models outside the ready method
        from .services import score_update
        bus = Bus()
        bus.set_on_message(score_update)
        bus.daemon = True
        bus.start()
