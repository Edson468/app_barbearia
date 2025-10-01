# Generated migration to create Service model based on current models.py

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('service_type', models.CharField(max_length=100)),
                ('barber', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('estimated_time', models.IntegerField()),
                ('appointment_datetime', models.DateTimeField(null=True, blank=True)),
                ('payment_method', models.CharField(max_length=20, null=True, blank=True)),
                ('payment_date', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
