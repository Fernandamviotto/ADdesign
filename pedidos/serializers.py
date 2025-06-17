from rest_framework import serializers
from .models import Pedido, Fornecedor, ProdutoServico

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
