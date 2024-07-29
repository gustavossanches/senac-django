from django import forms
from .models import Contato, Usuario

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = "__all__"
        

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        widgets = {
            "senha" : forms.PasswordInput(),
        }
        