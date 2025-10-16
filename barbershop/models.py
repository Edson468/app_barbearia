# barbershop/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # NOVO: Necessário para a data padrão da despesa

# Opções para a forma de pagamento
PAYMENT_CHOICES = [
    ('credito', 'Cartão de Crédito'),
    ('debito', 'Cartão de Débito'),
    ('pix', 'Pix'),
    ('dinheiro', 'Dinheiro'),
]

class Client(models.Model):
    """Modelo para armazenar informações dos clientes."""
    name = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    phone_whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name="Fone/WhatsApp")

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    """Modelo para os tipos de serviço oferecidos."""
    name = models.CharField(max_length=100, verbose_name="Nome do Serviço")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço")
    estimated_time = models.IntegerField(verbose_name="Tempo Estimado (minutos)")

    def __str__(self):
        return f"{self.name} (R$ {self.price})"

class Service(models.Model):
    client_name = models.CharField(max_length=100, verbose_name="Nome do Cliente")
    service_types = models.ManyToManyField(ServiceType, related_name='appointments', verbose_name="Tipos de Serviço")
    barber = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='services') 
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Preço Final")
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, verbose_name="Desconto (R$)")
    appointment_datetime = models.DateTimeField(null=True, blank=True)
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Serviço para {self.client_name} em {self.appointment_datetime}"

# ----------------------------------------------------------------------
# NOVO MODELO: Despesas da Barbearia
# ----------------------------------------------------------------------
class Expense(models.Model):
    """Modelo para registrar despesas operacionais da barbearia."""
    description = models.CharField(max_length=255, verbose_name="Descrição da Despesa")
    # Usa max_digits=10 para um limite de valor mais seguro
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Retirado (R$)") 
    # Usa DateField para registrar a data da despesa (necessário para filtro no caixa)
    expense_date = models.DateField(default=timezone.now, verbose_name="Data da Despesa") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Despesa: {self.description} - R${self.value}"

    class Meta:
        # Ordena as despesas da mais recente para a mais antiga por padrão
        ordering = ['-expense_date']