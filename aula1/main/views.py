from django.shortcuts import render, redirect
from .forms import ContatoForm, UsuarioForm
from .conectar import conectar_banco
from .forms import ContatoForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout  # Use Django authentication
from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required  # For 'login_required' decorator
from django.views.decorators.csrf import csrf_protect  # Adicione esta linha
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.db import transaction  # Para transações atômicas
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

def login(request):
    request.session['id'] = ''
    form = UsuarioForm()
    return render(request, 'main/login.html', {'form': form})

def processa_login(request):
    banco = conectar_banco()
    cursor = banco.cursor()
    
    email = request.POST['email']
    senha = request.POST['senha']

    dados = (email, senha)
    sql = 'SELECT * FROM usuarios WHERE email=%s AND senha=%s;'
    cursor.execute(sql, dados)
    
    usuario_existe = cursor.fetchone()
    print(f'USUARIO ->> {usuario_existe}')
    
    cursor.close()
    banco.close()
    if usuario_existe:
        print('login realizado!!')
        print(usuario_existe[0])
        request.session['id'] = usuario_existe[0]
        print(request.session['id'])
        # session['usuario_id'] = usuario_existe[0]

        return redirect('home')
    else:
        print('usuario nao cadastrado!')
        return redirect('login')
            

def home(request):
    #validação do login
    if not request.session.get('id'):
        return redirect('login')
    else:
        return render(request, 'main/home.html')

    
    
    
def mostrar_contatos(request):
    print(f'SESSION ID -> {request.session['id']}')
    banco = conectar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM contatos WHERE situacao = 'Em espera';")
    sql = cursor.fetchall()

    banco.close()
    cursor.close()
    return render(request, 'main/mostrar_contatos.html', {'sql': sql})

def contatos(request):
    form = ContatoForm()
    return render(request, 'main/contatos.html', {'form': form})