from django.urls import path
from . import views

app_name = 'barbershop'

urlpatterns = [
    # Autenticação
    path('', views.tela_login, name='login'), # Rota raiz agora aponta para o login
    path('register/', views.register_view, name='register'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Serviços / Agendamentos
    path('agendamentos/', views.service_list, name='service_list'),
    path('services/add/', views.service_form_view, name='add_service'),
    path('services/edit/<int:pk>/', views.service_form_view, name='edit_service'),
    path('services/delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('services/pay/<int:pk>/', views.mark_as_paid, name='mark_as_paid'),

    # Clientes
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/edit/<int:pk>/', views.edit_client, name='edit_client'),
    path('clients/delete/<int:pk>/', views.delete_client, name='delete_client'),

    # Tipos de Serviço
    path('service-types/', views.service_type_list, name='service_type_list'),
    path('service-types/add/', views.add_service_type, name='add_service_type'),
    path('service-types/edit/<int:pk>/', views.edit_service_type, name='edit_service_type'),
    path('service-types/delete/<int:pk>/', views.delete_service_type, name='delete_service_type'),

    # Barbeiros
    path('barbers/add/', views.add_barber, name='add_barber'),

    # Caixa e Exportação
    path('caixa/', views.daily_cashier, name='daily_cashier'),
    path('caixa/export/csv/', views.export_cashier_csv, name='export_cashier_csv'),
]