💈 BarberApp - Sistema de Gestão para Barbearia
Versão Django Versão Python Banco de dados Repositório GitHub

💡 Sobre o Projeto
O BarberApp é um sistema de gerenciamento completo e robusto, desenvolvido em Django , projetado para modernizar e otimizar o dia a dia de barbearias. Ele oferece uma solução integrada para controlar todas as operações, desde o agendamento de clientes até a gestão financeira .

⚡Principais Funcionalidades
Controle total e intuitivo das operações da sua barbearia:

📅 Gestão de Agendamentos
Agendamento rápido e fácil de horários.
Controle de disponibilidade de horários e profissionais.
Histórico completo de agendamentos.
👥 Cadastro de Clientes
Cadastro detalhado de clientes com informações de contato.
Acesso ao histórico de serviços realizados.
💇 Serviços e Produtos
Cadastro e gerenciamento de serviços (corte, barba, tratamentos, etc.).
Controle de produtos vendidos e em estoque.
Gestão de preços.
💰 Gestão Financeira
Controle de caixa e movimentações diárias.
Relatórios financeiros para análise de desempenho.
🛠️ Tecnologias Utilizadas
Este projeto foi construído com as seguintes ferramentas e frameworks:

Categoria	Tecnologia	Versão
Backend	Django	4.2
Linguagem	Python	3.8+
Banco de dados	SQLite	Nativo (Desenvolvimento)
Front-end	HTML, CSS	(CSS personalizado em static/css/sidebar.css)
📁 Estrutura do Projeto
O projeto é organizado seguindo o padrão do Django, utilizando aplicativos separados para maior clareza e manutenção.


barberapp/

├── app/                          \# Diretório principal (configurações globais)

│   ├── settings.py              \# Configurações do Django

│   ├── urls.py                  \# URLs principais

│   └── barbershop/              \# App: Core (Clientes, Agendamentos, Finanças)

│       ├── migrations/

│       ├── models.py            \# Modelos de dados

│       ├── views.py             \# Lógica das views (rotas)

│       └── urls.py              \# URLs do app 'barbershop'

├── products/                    \# App: Gerenciamento de Produtos e Estoque

│   ├── migrations/

│   ├── models.py

│   ├── views.py

│   └── urls.py

├── templates/                   \# Templates HTML

│   ├── barbershop/             \# Templates do app 'barbershop'

│   └── products/               \# Templates do app 'products'

├── static/                      \# Arquivos estáticos

│   └── css/

│       └── sidebar.css         \# CSS personalizado

├── venv/                       \# Ambiente virtual

├── db.sqlite3                  \# Banco de dados (desenvolvimento)

├── manage.py                   \# Script de gerenciamento do Django

└── requirements.txt            \# Dependências

🚀 Instalação e Configuração
Siga os passos abaixo para rodar o BarberApp localmente.

Pré-requisitos
Python (3.8 ou superior)
pip (gerenciador de pacotes Python)
Passos para Instalação
Clone ou repositório:

git clone [https://github.com/Edson468/barberapp.git](https://github.com/Edson468/barberapp.git)
cd barberapp
Crie e Ative o Ambiente Virtual:

# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/Mac
python3 -m venv venv
source venv/bin/activate
Instalar as dependências:

pip install -r requirements.txt
Execute as migrações do banco de dados:

python manage.py migrate
Crie um superusuário para acessar o Admin:

python manage.py createsuperuser
Execute o servidor de desenvolvimento:

python manage.py runserver
Após a execução, acesse o sistema em seu navegador:http://localhost:8000

📋 Como Usar
Acesso Inicial: Acesse a área de administração http://localhost:8000/adminusando o superusuário criado.
Configuração: Cadastro de serviços e produtos essenciais.
Gestão: Utilize uma interface para gerenciar clientes, agendamentos e acompanhar o controle financeiro.
👤 Desenvolvedor
Desenvolvido com dedicação por:

Edson - GitHub: Edson468

⭐ Apoie o Projeto
Se o BarberApp foi útil para você ou para sua estrela, considere deixar um neste repositório!
