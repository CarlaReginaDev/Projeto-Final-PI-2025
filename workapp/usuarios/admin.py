# usuarios/admin.py
from django.contrib import admin
from .models import Cliente, Login_Usuario, Pedidos, Notificacao

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'tipo', 'status', 'data_de_entrada', 'valor_orcamento']
    list_filter = ['tipo', 'status', 'data_de_entrada']
    search_fields = ['cliente__nome', 'tipo']
    list_editable = ['status']  # Permite editar status direto na lista
    actions = ['marcar_como_aceito', 'marcar_como_recusado']
    
    # Ações personalizadas
    def marcar_como_aceito(self, request, queryset):
        queryset.update(status=Pedidos.StatusPedido.ACEITO)
        for pedido in queryset:
            # Cria notificação para o cliente
            Notificacao.objects.create(
                usuario=pedido.cliente.user,
                pedido=pedido,
                mensagem=f"Seu pedido #{pedido.id} foi ACEITO! Em breve entraremos em contato.",
                tipo='SUCESSO'
            )
        self.message_user(request, f"{queryset.count()} pedidos marcados como aceitos.")
    marcar_como_aceito.short_description = "Marcar pedidos selecionados como ACEITOS"
    
    def marcar_como_recusado(self, request, queryset):
        queryset.update(status=Pedidos.StatusPedido.RECUSADO)
        for pedido in queryset:
            Notificacao.objects.create(
                usuario=pedido.cliente.user,
                pedido=pedido,
                mensagem=f"Seu pedido #{pedido.id} foi RECUSADO. Entre em contato para mais informações.",
                tipo='ALERTA'
            )
        self.message_user(request, f"{queryset.count()} pedidos marcados como recusados.")
    marcar_como_recusado.short_description = "Marcar pedidos selecionados como RECUSADOS"

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'endereco']
    search_fields = ['nome', 'telefone']

@admin.register(Login_Usuario)
class LoginUsuarioAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'created_at']
    search_fields = ['email', 'username__nome']

