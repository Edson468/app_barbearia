# barbershop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User # Necessário para o Barbeiro
from django.urls import reverse
from django.utils import timezone # CRÍTICO: Necessário para usar timezone.now()
from datetime import datetime
from django.db.models import Sum, Count # CRÍTICO: Necessário para a lógica do Caixa
from urllib.parse import urlencode
from django.http import HttpResponse
import csv
from .models import Service, Client, ServiceType, PAYMENT_CHOICES
from .forms import ServiceForm, ClientForm, BarberCreationForm, ServiceTypeForm

# Funções de Autenticação
# ----------------------------------------------------------------------
def tela_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('barbershop:service_list')
    else:
        form = AuthenticationForm()
    return render(request, 'barbershop/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = BarberCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('barbershop:service_list')
    else:
        form = BarberCreationForm()
    return render(request, 'barbershop/register.html', {'form': form})


def custom_logout_view(request):
    """View customizada que chama o logout do Django."""
    logout(request)
    return redirect('barbershop:login')


# Funções de Serviço (CRUD)
# ----------------------------------------------------------------------
@login_required
def service_list(request):
    filter_date_str = request.GET.get('filter_date')

    if filter_date_str:
        try:
            selected_date = datetime.strptime(filter_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    # Filtra todos os serviços para a data selecionada
    services_on_date = Service.objects.filter(appointment_datetime__date=selected_date)

    # Separa em pendentes (não pagos) e concluídos (pagos)
    pending_services = services_on_date.filter(payment_date__isnull=True).order_by('appointment_datetime')
    completed_services = services_on_date.filter(payment_date__isnull=False).order_by('appointment_datetime')
    
    context = {
        'selected_date': selected_date,
        'filter_date_str': filter_date_str,
        'pending_services': pending_services,
        'completed_services': completed_services,
        'payment_choices': PAYMENT_CHOICES,
        'today_str': timezone.now().strftime('%Y-%m-%d')
    }
    return render(request, 'barbershop/service_list.html', context)


@login_required
def service_form_view(request, pk=None):
    """View unificada para adicionar e editar serviços."""
    if pk:
        # Edição
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(request.POST or None, instance=service)
    else:
        # Adição
        service = None
        form = ServiceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)

            # Calcula/Recalcula o preço total
            total_price = 0
            for service_type in form.cleaned_data['service_types']:
                total_price += service_type.price

            instance.price = total_price - form.cleaned_data.get('discount', 0)
            instance.save()
            form.save_m2m()  # Salva a relação ManyToMany
            return redirect('barbershop:service_list')

    clients = Client.objects.all().values('name')
    service_types_prices = {st.id: st.price for st in ServiceType.objects.all()}
    all_services_list = list(ServiceType.objects.values('pk', 'name'))

    context = {
        'form': form,
        'clients': clients,
        'service_types_prices': service_types_prices,
        'all_services': all_services_list,
        'service': service, # Passa a instância para o template, útil para o título da página
    }
    return render(request, 'barbershop/add_service.html', context)


@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
    return redirect('barbershop:service_list')


# Funções de Cliente (CRUD)
# ----------------------------------------------------------------------
@login_required
def client_list(request):
    clients = Client.objects.all().order_by('name')
    return render(request, 'barbershop/client_list.html', {'clients': clients})


@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barbershop:client_list')
    else:
        form = ClientForm()
    return render(request, 'barbershop/add_client.html', {'form': form})


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('barbershop:client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'barbershop/add_client.html', {'form': form})


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
    return redirect('barbershop:client_list')


# Funções de Tipos de Serviço (CRUD)
# ----------------------------------------------------------------------
@login_required
def service_type_list(request):
    """Lista todos os tipos de serviço."""
    service_types = ServiceType.objects.all().order_by('name')
    context = {'service_types': service_types}
    return render(request, 'barbershop/service_type_list.html', context)


@login_required
def add_service_type(request):
    """Adiciona um novo tipo de serviço."""
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barbershop:service_type_list')
    else:
        form = ServiceTypeForm()
    return render(request, 'barbershop/add_service_type.html', {'form': form, 'is_new': True})


@login_required
def edit_service_type(request, pk):
    """Edita um tipo de serviço existente."""
    service_type = get_object_or_404(ServiceType, pk=pk)
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, instance=service_type)
        if form.is_valid():
            form.save()
            return redirect('barbershop:service_type_list')
    else:
        form = ServiceTypeForm(instance=service_type)
    return render(request, 'barbershop/add_service_type.html', {'form': form, 'is_new': False})


@login_required
def delete_service_type(request, pk):
    """Exclui um tipo de serviço."""
    service_type = get_object_or_404(ServiceType, pk=pk)
    if request.method == 'POST':
        service_type.delete()
    return redirect('barbershop:service_type_list')

# Funções de Barbeiro
# ----------------------------------------------------------------------
@login_required
def add_barber(request):
    if request.method == 'POST':
        form = BarberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Idealmente, redirecionar para uma lista de barbeiros
            return redirect('barbershop:service_list') 
    else:
        form = BarberCreationForm()
    return render(request, 'barbershop/add_barber.html', {'form': form})


# Funções de Pagamento e Caixa
# ----------------------------------------------------------------------
@login_required
def mark_as_paid(request, pk):
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=pk)
        payment_method = request.POST.get('payment_method')
        
        if payment_method:
            service.payment_method = payment_method
            service.payment_date = timezone.now()
            service.save()
            
            # Redireciona para o caixa do dia em que foi pago
            redirect_url = f"{reverse('barbershop:daily_cashier')}?filter_date={service.payment_date.strftime('%Y-%m-%d')}"
            return redirect(redirect_url)

    return redirect('barbershop:service_list')


def _get_filtered_cashier_services(request):
    """Função auxiliar para obter serviços de caixa filtrados."""
    
    filter_date = request.GET.get('filter_date', '').strip()
    filter_month = request.GET.get('filter_month', '').strip()
    filter_service_type = request.GET.get('filter_service_type', '').strip()
    filter_barber = request.GET.get('filter_barber', '').strip()
    filter_payment_method = request.GET.get('filter_payment_method', '').strip()
    
    has_filters = any([filter_date, filter_month, filter_service_type, filter_payment_method, filter_barber])
    
    # Seleciona os serviços e seus respectivos barbeiros para otimizar a consulta
    services_query = Service.objects.prefetch_related('service_types').select_related('barber').filter(payment_date__isnull=False)

    if has_filters:
        if filter_date:
            services_query = services_query.filter(payment_date__date=filter_date)
        elif filter_month:
            try:
                year, month = map(int, filter_month.split('-'))
                services_query = services_query.filter(payment_date__year=year, payment_date__month=month)
            except ValueError:
                pass
        
        if filter_service_type:
            services_query = services_query.filter(service_types__id=filter_service_type)

        if filter_barber:
            services_query = services_query.filter(barber_id=filter_barber)
        
        if filter_payment_method:
            services_query = services_query.filter(payment_method=filter_payment_method)
    else:
        # Padrão: serviços pagos hoje
        today = timezone.now().date()
        services_query = services_query.filter(payment_date__date=today)

    return services_query.order_by('-payment_date')


@login_required
def daily_cashier(request):
    
    services_today = _get_filtered_cashier_services(request)
    
    aggregation = services_today.aggregate(total_value=Sum('price'), total_services=Count('id'))
    total_value = aggregation.get('total_value') or 0
    total_services = aggregation.get('total_services') or 0

    context = {
        'services_today': services_today,
        'total_value': total_value,
        'total_services': total_services,
        'service_types': ServiceType.objects.all().order_by('name'),
        'barbers': User.objects.all().order_by('username'),
        'payment_methods': PAYMENT_CHOICES,
        # Passa os parâmetros GET para o template para construir os links de exportação
        'query_params': request.GET.urlencode(),
        'filter_date': request.GET.get('filter_date', '').strip(),
        'filter_month': request.GET.get('filter_month', '').strip(),
        'filter_service_type': request.GET.get('filter_service_type', '').strip(),
        'filter_barber': request.GET.get('filter_barber', '').strip(),
        'filter_payment_method': request.GET.get('filter_payment_method', '').strip(),
        'has_filters': any([request.GET.get(key) for key in ['filter_date', 'filter_month', 'filter_service_type', 'filter_barber', 'filter_payment_method']]),
    }
    return render(request, 'barbershop/daily_cashier.html', context)


@login_required
def export_cashier_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="caixa_{timezone.now().strftime("%Y-%m-%d")}.csv"'
    
    # Adiciona BOM para compatibilidade com Excel
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Data Pagamento', 'Cliente', 'Barbeiro', 'Serviço', 'Forma Pag.', 'Valor (R$)'])

    services = _get_filtered_cashier_services(request)
    # Calcula o total para adicionar no final
    total_value = services.aggregate(total=Sum('price'))['total'] or 0

    for service in services:
        writer.writerow([
            service.payment_date.strftime('%d/%m/%Y %H:%M'),
            service.client_name,
            service.barber.username if service.barber else 'N/A',
            ", ".join([st.name for st in service.service_types.all()]),
            service.get_payment_method_display(),
            str(service.price).replace('.', ',')
        ])
    
    # Adiciona a linha de total no final do CSV
    writer.writerow(['', '', '', '', 'Total', str(total_value).replace('.', ',')])

    return response