"""
Esse arquivo de migração anterior referenciava o app 'products' que não existe no projeto atual.
Para manter consistência, deixamos uma migração vazia que depende da 0001 criada acima.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barbershop', '0001_initial'),
    ]

    operations = []
