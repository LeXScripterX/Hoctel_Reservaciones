from django.apps import AppConfig


class BaseHotelesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_Hoteles'

    def ready(self):
      import base_Hoteles.signals 