from django.contrib import admin
from .models import Cliente, Login_Usuario, Consoles, Controles, Outros

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'endereco']
    search_fields = ['nome', 'telefone']

@admin.register(Login_Usuario)
class LoginUsuarioAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'created_at']
    search_fields = ['email', 'username__nome']

@admin.register(Consoles)
class ConsolesAdmin(admin.ModelAdmin):
    list_display = ['nome_cliente', 'tipo_console', 'data_de_entrada', 'valor_orcamento']
    list_filter = ['data_de_entrada', 'data_saida']

@admin.register(Controles)
class ControlesAdmin(admin.ModelAdmin):
    list_display = ['nome_cliente', 'tipo_controle', 'data_de_entrada', 'valor_orcamento']
    list_filter = ['data_de_entrada', 'data_saida']

@admin.register(Outros)
class OutrosAdmin(admin.ModelAdmin):
    list_display = ['nome_cliente', 'tipo_outro', 'data_de_entrada', 'valor_orcamento']
    list_filter = ['data_de_entrada', 'data_saida']