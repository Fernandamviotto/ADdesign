from django import forms
from .models import Pedido, Fornecedor
from django.contrib.auth.models import User

TIPO_PEDIDO_CHOICES = [
    ('Receita', 'Receita'),
    ('Despesa', 'Despesa'),
    ('Serviço', 'Serviço'),
]

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['tipo', 'descricao', 'valor', 'data', 'fornecedor']

    tipo = forms.ChoiceField(choices=TIPO_PEDIDO_CHOICES)
    descricao = forms.CharField(max_length=255)
    valor = forms.DecimalField(max_digits=10, decimal_places=2)
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fornecedor = forms.ModelChoiceField(queryset=Fornecedor.objects.all(), required=False)

class FiltroForm(forms.Form):
    tipo = forms.ChoiceField(choices=[('', 'Todos')] + TIPO_PEDIDO_CHOICES, required=False)
    fornecedor = forms.CharField(max_length=255, required=False)
    usuario = forms.CharField(max_length=150, required=False)
    data_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
