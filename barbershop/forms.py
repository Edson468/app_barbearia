# barbershop/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Service, Client, ServiceType

class ServiceForm(forms.ModelForm):
    # Garante que o campo 'barber' seja uma lista de seleção de todos os usuários
    barber = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        label="Barbeiro",
        widget=forms.Select(attrs={'class': 'form-control'}) 
    )

    class Meta:
        model = Service
        # O campo 'price' será calculado na view, não preenchido pelo usuário diretamente.
        fields = ['client_name', 'service_types', 'barber', 'discount', 'appointment_datetime']
        labels = {
            'client_name': 'Nome do Cliente',
            'service_types': 'Tipos de Serviço',
            'discount': 'Desconto (R$)',
            'appointment_datetime': 'Data e Hora do Agendamento',
        }
        
        widgets = {
            'service_types': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'appointment_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            
            # CRÍTICO: Oculta os campos de pagamento
            'payment_method': forms.HiddenInput(),
            'payment_date': forms.HiddenInput(),
        }

    # Remove os labels dos campos ocultos no formulário
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'payment_method' in self.fields:
    #         del self.fields['payment_method']
    #     if 'payment_date' in self.fields:
    #         del self.fields['payment_date']

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['name', 'price', 'estimated_time']


class ClientForm(forms.ModelForm):
    """Formulário para criar e editar clientes."""
    class Meta:
        model = Client
        fields = ['name', 'phone_whatsapp']


class BarberCreationForm(UserCreationForm):
    """Formulário para criar usuários (barbeiros) a partir do painel."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }