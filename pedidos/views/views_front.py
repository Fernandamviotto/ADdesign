from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pedidos.models import Pedido, Fornecedor
from pedidos.forms import PedidoForm, FiltroForm

@login_required
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

@login_required
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
    return render(request, 'criar_pedido.html', {'form': form})

@login_required
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

@login_required
def detalhes_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'detalhes_pedido.html', {'pedido': pedido})
