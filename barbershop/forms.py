# barbershop/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Importe o novo modelo Expense
from .models import Service, Client, ServiceType, Expense 


class ServiceForm(forms.ModelForm):
    # Garante que o campo 'barber' seja uma lista de seleção de todos os usuários
    barber = forms.ModelChoiceField(
        queryset=User.objects.all(), 
        label="Barbeiro",
        widget=forms.Select(attrs={'class': 'form-control'}) 
    )

    class Meta:
        model = Service
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
            
            'payment_method': forms.HiddenInput(),
            'payment_date': forms.HiddenInput(),
        }
# ... (O método __init__ para remover campos ocultos no ServiceForm foi mantido comentado por enquanto, 
# mas se você o descomentar, ele deve ser incluído aqui.)
# ...


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

# ----------------------------------------------------------------------
# NOVO FORMULÁRIO: Despesas
# ----------------------------------------------------------------------
class ExpenseForm(forms.ModelForm):
    """Formulário para registrar despesas operacionais da barbearia."""
    class Meta:
        model = Expense
        fields = ['description', 'value', 'expense_date']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            # Define o input como tipo 'date' para seleção de calendário fácil
            'expense_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        }