import tempfile
import pandas as pd
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from pedidos.models import Pedido
from django.contrib.auth.decorators import login_required

@login_required
def exportar_pdf(request):
    pedidos = Pedido.objects.all()

    # Cálculos para o sumário
    total_lucro = sum(p.lucro() for p in pedidos)
    total_despesas = sum(p.despesas for p in pedidos)
    total_pedidos = pedidos.count()

    formato = request.GET.get('formato', 'pdf')

    if formato == 'excel':
        # Criação de DataFrame para exportação
        dados = []
        for pedido in pedidos:
            dados.append({
                'Cliente': pedido.cliente,
                'Serviço': pedido.servico,
                'Valor': pedido.valor,
                'Despesas': pedido.despesas,
                'Lucro': pedido.lucro(),
                'Data': pedido.data.strftime('%d/%m/%Y'),
            })

        df = pd.DataFrame(dados)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=relatorio_pedidos.xlsx'
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Pedidos')

        return response

    # Exportar como PDF (default)
    context = {
        'pedidos': pedidos,
        'total_lucro': total_lucro,
        'total_despesas': total_despesas,
        'total_pedidos': total_pedidos,
        'user': request.user,
    }

    html_string = render_to_string('pedidos/exportar_pdf.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))

    with tempfile.NamedTemporaryFile(suffix=".pdf") as output:
        html.write_pdf(target=output.name)
        output.seek(0)
        pdf = output.read()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_pedidos.pdf"'
    return response
