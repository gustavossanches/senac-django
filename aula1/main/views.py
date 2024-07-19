from django.shortcuts import render
from .forms import ContatoForm, UsuarioForm

def login(request):
    form = UsuarioForm()
    return render(request, 'main/login.html', {'form': form})

def home(request):
    return render(request, 'main/home.html')

def contatos(request):
    form = ContatoForm()
    return render(request, 'main/contatos.html', {'form': form})