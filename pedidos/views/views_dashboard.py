from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from pedidos.decorators import login_required_if_not_debug
from pedidos.models import Pedido
import json
import plotly.graph_objs as go
import plotly
from django.shortcuts import render

def dashboard_mock(request):
    return render(request, "dashboard.html")


@login_required_if_not_debug
def dashboard(request):
    user = request.user
    if user.is_superuser or user.groups.filter(name='admin').exists():
        pedidos = Pedido.objects.all()
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)

    total_lucro = pedidos.aggregate(lucro=Sum('valor'))['lucro'] or 0
    despesas = pedidos.filter(tipo='Despesa').aggregate(total=Sum('valor'))['total'] or 0
    quantidade_servicos = pedidos.filter(tipo='Serviço').count()

    # Dados para gráfico mensal
    pedidos_mes = pedidos.extra(select={'mes': "strftime('%%Y-%%m', data)"})
    receitas_mensais = pedidos_mes.filter(tipo='Receita').values('mes').annotate(total=Sum('valor')).order_by('mes')
    despesas_mensais = pedidos_mes.filter(tipo='Despesa').values('mes').annotate(total=Sum('valor')).order_by('mes')

    meses = [x['mes'] for x in receitas_mensais]
    valores_receita = [x['total'] for x in receitas_mensais]
    valores_despesa = [x['total'] for x in despesas_mensais]

    trace1 = go.Bar(x=meses, y=valores_receita, name='Receita')
    trace2 = go.Bar(x=meses, y=valores_despesa, name='Despesa')

    layout = go.Layout(barmode='group', title='Receitas x Despesas Mensais')

    graph_json = json.dumps({'data': [trace1, trace2], 'layout': layout}, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        'total_lucro': total_lucro,
        'despesas': despesas,
        'quantidade_servicos': quantidade_servicos,
        'graph_html': graph_json,
    }
    return render(request, 'dashboard.html', context)
