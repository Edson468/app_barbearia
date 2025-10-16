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
# ALTERAÇÃO CRÍTICA: Incluir Expense e ExpenseForm nas importações
from .models import Service, Client, ServiceType, PAYMENT_CHOICES, Expense 
from .forms import ServiceForm, ClientForm, BarberCreationForm, ServiceTypeForm, ExpenseForm 


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


# Funções de Despesa (NOVO)
# ----------------------------------------------------------------------
@login_required
def add_expense(request):
    """Adiciona uma nova despesa no sistema."""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            # Redireciona para o caixa do dia da despesa
            redirect_url = f"{reverse('barbershop:daily_cashier')}?filter_date={form.cleaned_data['expense_date'].strftime('%Y-%m-%d')}"
            return redirect(redirect_url)
    else:
        # Define a data atual como padrão no formulário
        form = ExpenseForm(initial={'expense_date': timezone.now().date()})
    
    return render(request, 'barbershop/add_expense.html', {'form': form})


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


def _get_filtered_cashier_transactions(request):
    """Função auxiliar para obter serviços (receitas) E despesas (saídas) filtrados."""
    
    filter_date = request.GET.get('filter_date', '').strip()
    filter_month = request.GET.get('filter_month', '').strip()
    filter_service_type = request.GET.get('filter_service_type', '').strip()
    filter_barber = request.GET.get('filter_barber', '').strip()
    filter_payment_method = request.GET.get('filter_payment_method', '').strip()
    
    has_filters = any([filter_date, filter_month, filter_service_type, filter_payment_method, filter_barber])
    
    # Base Query para RECEITAS (Serviços Pagos)
    services_query = Service.objects.prefetch_related('service_types').select_related('barber').filter(payment_date__isnull=False)
    # Base Query para DESPESAS
    expenses_query = Expense.objects.all()

    # Aplica Filtros de Data
    if has_filters:
        if filter_date:
            services_query = services_query.filter(payment_date__date=filter_date)
            expenses_query = expenses_query.filter(expense_date=filter_date)
        elif filter_month:
            try:
                year, month = map(int, filter_month.split('-'))
                services_query = services_query.filter(payment_date__year=year, payment_date__month=month)
                expenses_query = expenses_query.filter(expense_date__year=year, expense_date__month=month)
            except ValueError:
                pass
        
        # Filtros de Serviço/Pagamento/Barbeiro só se aplicam a serviços
        if filter_service_type:
            services_query = services_query.filter(service_types__id=filter_service_type)

        if filter_barber:
            services_query = services_query.filter(barber_id=filter_barber)
        
        if filter_payment_method:
            services_query = services_query.filter(payment_method=filter_payment_method)
    else:
        # Padrão: receitas e despesas de hoje
        today = timezone.now().date()
        services_query = services_query.filter(payment_date__date=today)
        expenses_query = expenses_query.filter(expense_date=today)

    return services_query, expenses_query # Retorna dois QuerySets


@login_required
def daily_cashier(request):
    
    # Obtém Receitas (services) e Despesas (expenses)
    services_query, expenses_query = _get_filtered_cashier_transactions(request)

    # 1. Cálculo de Totais
    income_aggregation = services_query.aggregate(total_income=Sum('price'), total_services=Count('id'))
    total_income = income_aggregation.get('total_income') or 0
    total_services = income_aggregation.get('total_services') or 0

    outcome_aggregation = expenses_query.aggregate(total_outcome=Sum('value'))
    total_outcome = outcome_aggregation.get('total_outcome') or 0

    # Total Líquido (Receitas - Despesas)
    final_total_value = total_income - total_outcome

    # 2. Combinação e Formatação para Display
    # Formata Receitas (valor positivo)
    services_list = [{
        'description': f"Receita: {s.client_name} - {', '.join([st.name for st in s.service_types.all()])}",
        'value': s.price,
        'is_expense': False,
        'barber': s.barber.username if s.barber else 'N/A',
        'payment_method': s.get_payment_method_display(),
        'date': s.payment_date.date(),
        'sort_time': s.payment_date 
    } for s in services_query]

    # Formata Despesas (valor negativo)
    expenses_list = [{
        'description': f"DESPESA: {e.description}",
        'value': -e.value, # Valor negativo
        'is_expense': True,
        'barber': 'N/A',
        'payment_method': 'N/A',
        'date': e.expense_date,
        # Cria um datetime para ordenação uniforme com as receitas
        'sort_time': timezone.make_aware(datetime.combine(e.expense_date, datetime.min.time())) 
    } for e in expenses_query]
    
    # Combina e ordena todas as transações (Receitas e Despesas) pela data/hora
    transactions_list = services_list + expenses_list
    transactions_list.sort(key=lambda x: x['sort_time'], reverse=True)

    context = {
        'transactions': transactions_list, # Nova lista combinada
        'total_value': final_total_value, # Total Líquido
        'total_income': total_income,     # Total de Receitas
        'total_outcome': total_outcome,   # Total de Despesas
        'total_services': total_services, # Total de serviços (agora só conta receitas)
        
        'service_types': ServiceType.objects.all().order_by('name'),
        'barbers': User.objects.all().order_by('username'),
        'payment_methods': PAYMENT_CHOICES,
        
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
    
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Data/Hora', 'Tipo', 'Descrição', 'Barbeiro', 'Forma Pag.', 'Valor (R$)'])

    # Obtém Receitas e Despesas
    services_query, expenses_query = _get_filtered_cashier_transactions(request)
    
    transactions_list = []

    # 1. Formata Receitas
    for s in services_query:
        transactions_list.append({
            'sort_time': s.payment_date,
            'data_hora': s.payment_date.strftime('%d/%m/%Y %H:%M'),
            'tipo': 'RECEITA',
            'descricao': f"{s.client_name} - {', '.join([st.name for st in s.service_types.all()])}",
            'barbeiro': s.barber.username if s.barber else 'N/A',
            'pagamento': s.get_payment_method_display(),
            'valor': s.price
        })

    # 2. Formata Despesas
    for e in expenses_query:
        transactions_list.append({
            'sort_time': timezone.make_aware(datetime.combine(e.expense_date, datetime.min.time())),
            'data_hora': e.expense_date.strftime('%d/%m/%Y'),
            'tipo': 'DESPESA',
            'descricao': e.description,
            'barbeiro': 'N/A',
            'pagamento': 'N/A',
            'valor': -e.value # Valor negativo para despesas
        })

    # Ordena todas as transações (Receitas e Despesas)
    transactions_list.sort(key=lambda x: x['sort_time'], reverse=True)

    # Calcula os totais
    total_income = services_query.aggregate(total=Sum('price'))['total'] or 0
    total_outcome = expenses_query.aggregate(total=Sum('value'))['total'] or 0
    final_total_value = total_income - total_outcome

    # Escreve as linhas de transação
    for t in transactions_list:
        writer.writerow([
            t['data_hora'],
            t['tipo'],
            t['descricao'],
            t['barbeiro'],
            t['pagamento'],
            # Formata o valor, garantindo o sinal de menos para despesas
            str(t['valor']).replace('.', ',') 
        ])
    
    # Adiciona as linhas de resumo
    writer.writerow([])
    writer.writerow(['', '', '', '', 'Total Receitas', str(total_income).replace('.', ',')])
    writer.writerow(['', '', '', '', 'Total Despesas', str(total_outcome).replace('.', ',')])
    writer.writerow(['', '', '', '', 'Total Líquido', str(final_total_value).replace('.', ',')])

    return response