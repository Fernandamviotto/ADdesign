from django.http import HttpResponse
import io
import csv
import xlsxwriter
from reportlab.pdfgen import canvas

def exportar_pdf(request):
    # Cria um buffer na memória
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "Relatório PDF - Exemplo básico")
    # Adicione mais conteúdo ao PDF aqui
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")

def exportar_excel(request):
    # Cria um buffer na memória
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Exemplo de cabeçalho e dados
    worksheet.write('A1', 'Nome')
    worksheet.write('B1', 'Quantidade')
    data = [
        ['Produto A', 10],
        ['Produto B', 20],
        ['Produto C', 30],
    ]

    row = 1
    for nome, quantidade in data:
        worksheet.write(row, 0, nome)
        worksheet.write(row, 1, quantidade)
        row += 1

    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=relatorio.xlsx'
    return response
