from django.apps import AppConfig
import os

class IrWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ir_web'

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":
            from ir_system.ir_system import IRSystem
            from . import registry
            registry.ir_instance = IRSystem()