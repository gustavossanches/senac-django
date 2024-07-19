from django.db import models
class Contato(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    mensagem = models.TextField()

class Usuario(models.Model):
    usuario = models.CharField(max_length=200)
    email = models.EmailField()
    senha = models.CharField(max_length=200)
    
