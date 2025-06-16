from django import forms
from .models import Pedido, Fornecedor
from django.contrib.auth.models import User

TIPO_PEDIDO_CHOICES = [
    ('Receita', 'Receita'),
    ('Despesa', 'Despesa'),
    ('Serviço', 'Serviço'),
]

class PedidoForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=TIPO_PEDIDO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    descricao = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descreva o serviço ou movimentação financeira...'
        })
    )
    valor = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Ex: 1000.00'
        })
    )
    data = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fornecedor = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Pedido
        fields = ['tipo', 'descricao', 'valor', 'data', 'fornecedor']

class FiltroForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=[('', 'Todos')] + TIPO_PEDIDO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fornecedor = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    usuario = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
