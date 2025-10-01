# 💈 BarberApp - Sistema de Gestão para Barbearia

[![Django Version](https://img.shields.io/badge/Django-4.2-green)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Database](https://img.shields.io/badge/SQLite-Database-003B57)](https://www.sqlite.org/index.html)
[![GitHub Repository](https://img.shields.io/badge/Repositório-Edson468%2Fbarberapp-informational)](https://github.com/Edson468/barberapp)

## 💡 Sobre o Projeto

O **BarberApp** é um sistema de gestão completo e robusto, desenvolvido em **Django**, projetado para modernizar e otimizar o dia a dia de barbearias. Ele oferece uma solução integrada para controlar todas as operações, desde o **agendamento de clientes** até a **gestão financeira**.

## ⚡ Principais Funcionalidades

Controle total e intuitivo das operações da sua barbearia:

### 📅 Gestão de Agendamentos
* Agendamento rápido e fácil de horários.
* Controle de **disponibilidade** de horários e profissionais.
* Histórico completo de agendamentos.

### 👥 Cadastro de Clientes
* Cadastro detalhado de clientes com informações de contato.
* Acesso ao **histórico de serviços** realizados.

### 💇 Serviços e Produtos
* Cadastro e gerenciamento de serviços (corte, barba, tratamentos, etc.).
* **Controle de produtos** vendidos e em estoque.
* Gestão de preços.

### 💰 Gestão Financeira
* Controle de **caixa** e movimentações diárias.
* **Relatórios financeiros** para análise de desempenho.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com as seguintes ferramentas e frameworks:

| Categoria | Tecnologia | Versão |
| :--- | :--- | :--- |
| **Backend** | **Django** | 4.2 |
| **Linguagem** | **Python** | 3.8+ |
| **Database** | **SQLite** | Nativo (Desenvolvimento) |
| **Frontend** | HTML, CSS | (CSS personalizado em `static/css/sidebar.css`) |

## 📁 Estrutura do Projeto

O projeto é organizado seguindo o padrão do Django, utilizando *apps* separados para maior clareza e manutenção.

barberapp/

├── app/                          # Diretório principal (configurações globais)

│   ├── settings.py              # Configurações do Django

│   ├── urls.py                  # URLs principais

│   └── barbershop/              # App: Core (Clientes, Agendamentos, Finanças)

│       ├── migrations/

│       ├── models.py            # Modelos de dados

│       ├── views.py             # Lógica das views (rotas)

│       └── urls.py              # URLs do app 'barbershop'

├── products/                    # App: Gerenciamento de Produtos e Estoque

│   ├── migrations/

│   ├── models.py

│   ├── views.py

│   └── urls.py

├── templates/                   # Templates HTML

│   ├── barbershop/             # Templates do app 'barbershop'

│   └── products/               # Templates do app 'products'

├── static/                      # Arquivos estáticos

│   └── css/

│       └── sidebar.css         # CSS personalizado

├── venv/                       # Ambiente virtual

├── db.sqlite3                  # Banco de dados (desenvolvimento)

├── manage.py                   # Script de gerenciamento do Django

└── requirements.txt            # Dependências

## 🚀 Instalação e Configuração

Siga os passos abaixo para rodar o **BarberApp** localmente.

### Pré-requisitos
* **Python** (3.8 ou superior)
* **pip** (gerenciador de pacotes Python)

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Edson468/barberapp.git](https://github.com/Edson468/barberapp.git)
    cd barberapp
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    # No Windows
    python -m venv venv
    venv\Scripts\activate

    # No Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário para acessar o Admin:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Execute o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

Após a execução, acesse o sistema em seu navegador: **`http://localhost:8000`**

## 📋 Como Usar

1.  **Acesso Inicial:** Acesse a área de administração em **`http://localhost:8000/admin`** usando o superusuário criado.
2.  **Configuração:** Cadastre serviços e produtos essenciais.
3.  **Gestão:** Utilize a interface para gerenciar clientes, agendamentos e acompanhar o controle financeiro.

## 👤 Desenvolvedor

Desenvolvido com dedicação por:

**Edson** - [GitHub: Edson468](https://github.com/Edson468)

## ⭐ Apoie o Projeto

Se o **BarberApp** foi útil para você ou te inspirou, considere deixar uma **estrela** neste repositório!
