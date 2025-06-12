from django.db import models
from django.contrib.auth.models import User

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    contato = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    TIPO_CHOICES = [
        ('Receita', 'Receita'),
        ('Despesa', 'Despesa'),
        ('Serviço', 'Serviço'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.descricao} - R$ {self.valor}"
