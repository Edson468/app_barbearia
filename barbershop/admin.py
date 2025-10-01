# barbershop/admin.py

from django.contrib import admin
from . import models

# 1. Defina uma classe de Admin para o seu modelo Service (opcional, mas bom)
class ServiceAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de serviços no painel admin
    list_display = ('client_name', 'display_service_types', 'barber', 'price', 'appointment_datetime', 'payment_method', 'payment_date')
    # Campos que podem ser usados para filtrar
    list_filter = ('barber', 'payment_method', 'service_types')
    # Campos que podem ser pesquisados
    search_fields = ('client_name', 'service_types__name')
    
    # Define a ordem dos campos no formulário de edição/criação
    fieldsets = (
        (None, {'fields': ('client_name', 'service_types', 'barber', 'price', 'discount', 'appointment_datetime')}),
        ('Informações de Pagamento', {'fields': ('payment_method', 'payment_date'), 'classes': ('collapse',)}),
    )

    def display_service_types(self, obj):
        """Cria uma string com os nomes dos serviços para o list_display."""
        return ", ".join([st.name for st in obj.service_types.all()])
    
    display_service_types.short_description = 'Tipos de Serviço'


# 2. Registre o modelo Service
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Client)
admin.site.register(models.ServiceType)

# 3. Certifique-se de que não há código para 'Product' ou 'ProductAdmin'