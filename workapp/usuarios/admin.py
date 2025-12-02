from django.contrib import admin
from .models import Cliente, Login_Usuario

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'endereco']
    search_fields = ['nome', 'telefone']

@admin.register(Login_Usuario)
class LoginUsuarioAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'created_at']
    search_fields = ['email', 'username__nome']
