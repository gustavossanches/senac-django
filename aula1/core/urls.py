"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.page_login, name='page_login'),
    path('page_home', views.page_home, name='page_home'),
    path('processa_login', views.processa_login, name='processa_login'),
    path('processa_cadastro', views.processa_cadastro, name='processa_cadastro'),
    path('processa_criar_chamados', views.processa_criar_chamados, name='processa_criar_chamados'),
    # path('page_atualizar_usuario/<int:id>', views.page_atualizar_usuario, name='page_atualizar_usuario'),
    
    path('page_mostrar_meus_chamados', views.page_mostrar_meus_chamados, name='page_mostrar_meus_chamados'),
    path('page_mostrar_chamados', views.page_mostrar_chamados, name='page_mostrar_chamados'),
    path('page_mostrar_usuarios', views.page_mostrar_usuarios, name='page_mostrar_usuarios'),
    path('page_criar_chamado', views.page_criar_chamado, name='page_criar_chamado'),
    path('page_cadastro', views.page_cadastro, name='page_cadastro'),
    path('atribui_atendimento/<int:id>/', views.atribui_atendimento, name='atribui_atendimento'),
    path('page_atualizar_usuario/<int:id>', views.page_atualizar_usuario, name='page_atualizar_usuario'),
    path('finalizar_chamado/<int:id>', views.finalizar_chamado, name='finalizar_chamado'),
    path('processa_atualizar_usuario/<int:id>', views.processa_atualizar_usuario, name='processa_atualizar_usuario'),
    path('excluir_usuario/<int:id>', views.excluir_usuario, name='excluir_usuario'),
    
    path('lista_admin', views.lista_admin, name='lista_admin'),
]
