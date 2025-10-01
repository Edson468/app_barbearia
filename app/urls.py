# app/urls.py

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta linha é a chave para o roteamento do seu app
    path('', include('barbershop.urls', namespace='barbershop')), 
]