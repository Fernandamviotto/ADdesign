from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pedidos.decorators import login_required_if_not_debug
from pedidos.models import Pedido, Fornecedor
from pedidos.forms import PedidoForm, FiltroForm
from django.shortcuts import render

import os



USE_MOCK = os.getenv("USE_MOCK_DATA") == "True"

def listar_pedidos(request):
    if USE_MOCK:
        pedidos = [
            {'id': 1, 'titulo': 'Pedido Mock 1', 'descricao': 'Descrição mock 1', 'valor': 100.0},
            {'id': 2, 'titulo': 'Pedido Mock 2', 'descricao': 'Descrição mock 2', 'valor': 200.0},
        ]
    else:
        pedidos = supabase_client.get_pedidos()  # Exemplo de chamada real
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})


@login_required_if_not_debug
def listar_pedidos(request):
    form = FiltroForm(request.GET or None)
    pedidos = Pedido.objects.all()

    if form.is_valid():
        tipo = form.cleaned_data.get('tipo')
        fornecedor = form.cleaned_data.get('fornecedor')
        usuario = form.cleaned_data.get('usuario')
        data_inicio = form.cleaned_data.get('data_inicio')
        data_fim = form.cleaned_data.get('data_fim')

        if tipo:
            pedidos = pedidos.filter(tipo=tipo)
        if fornecedor:
            pedidos = pedidos.filter(fornecedor__nome__icontains=fornecedor)
        if usuario:
            pedidos = pedidos.filter(usuario__username__icontains=usuario)
        if data_inicio:
            pedidos = pedidos.filter(data__gte=data_inicio)
        if data_fim:
            pedidos = pedidos.filter(data__lte=data_fim)

    context = {
        'pedidos': pedidos,
        'form': form
    }
    return render(request, 'listar_pedidos.html', context)

@login_required_if_not_debug
def criar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            messages.success(request, 'Pedido criado com sucesso.')
            return redirect('pedidos:listar_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/criar_pedido.html', {'form': form})

@login_required_if_not_debug
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido atualizado com sucesso.')
            return redirect('pedidos:listar_pedidos')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'editar_pedido.html', {'form': form})

@login_required_if_not_debug
def detalhes_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'detalhes_pedido.html', {'pedido': pedido})


def dashboard_mock(request):
    # Dados fixos só para visualização
    context = {
        'lucro_total': 15000.00,
        'despesas_totais': 7000.00,
        'quantidade_servicos': 45,
        'grafico_evolucao': {
            'meses': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'valores': [2000, 2500, 2200, 3000, 2800, 3500],
        }
    }
    return render(request, 'dashboard.html', context)