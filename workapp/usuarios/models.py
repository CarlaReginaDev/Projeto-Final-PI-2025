from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=150, verbose_name="Nome Completo")
    telefone = models.CharField(max_length=15, verbose_name="Telefone", null=False, primary_key=True)
    endereco = models.CharField(max_length=255, verbose_name="Endereço", null=False)

    
    class Meta:
        app_label = 'usuarios'
    
    def __str__(self):
        return self.nome

class Login_Usuario(models.Model):
    username = models.OneToOneField(Cliente, on_delete=models.CASCADE, verbose_name="Nome de Usuário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    email = models.EmailField(unique=True, verbose_name="Email", primary_key=True)
    
    class Meta:
        app_label = 'usuarios'
    
    def __str__(self):
        return self.email

class Pedidos(models.Model):
    # 1. Defina as opções como uma classe de tuplas
    class TiposPedidos(models.TextChoices):
        CONSOLE = 'CON', 'Console'
        OUTROS = 'OUT', 'Acessórios/Outros'
    
    # 🌟 MUDANÇA CRÍTICA: Associe o pedido ao objeto Cliente
    cliente = models.ForeignKey(
        Cliente, # O nome do modelo (Cliente)
        on_delete=models.CASCADE,
        verbose_name="Cliente"
    ) 
    
    # Remova nome_cliente (ou use-o para fins de relatórios se for necessário)
    # nome_cliente = models.CharField(max_length=150, verbose_name="Nome do cliente") # <-- REMOVER
    
    tipo = models.CharField(
        max_length=3,
        choices=TiposPedidos.choices,
        default=TiposPedidos.CONSOLE,
        verbose_name="Tipo de Pedido"
    )
    
    data_de_entrada = models.DateField(auto_now_add=True, verbose_name="Data de Entrada")
    detalhes_orcamento = models.TextField(verbose_name="Detalhes do Orçamento")
    valor_orcamento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Orçamento", null=True, blank=True)
    data_saida = models.DateField(null=True, blank=True, verbose_name="Data de Saída")
    
    class Meta:
        app_label = 'usuarios'
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.get_tipo_display()}"