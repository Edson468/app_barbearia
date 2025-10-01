# barbershop/apps.py

from django.apps import AppConfig

class BarbershopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Renomeie esta linha para 'barbershop'
    name = 'barbershop'