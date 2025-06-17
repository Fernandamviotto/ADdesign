from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido', 'status', 'valor_total')
    list_filter = ('status', 'data_pedido')
    search_fields = ('cliente__nome', 'id')
    ordering = ('-data_pedido',)
    readonly_fields = ('data_criacao', 'data_atualizacao')

    fieldsets = (
        (None, {
            'fields': ('cliente', 'descricao', 'valor_total')
        }),
        ('Status e Datas', {
            'fields': ('status', 'data_pedido', 'data_criacao', 'data_atualizacao')
        }),
    )