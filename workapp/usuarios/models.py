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
    # ... (outras configurações)
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
    
    class StatusPedido(models.TextChoices):
        PENDENTE = 'PEN', 'Pendente'
        ACEITO = 'ACE', 'Aceito'
        RECUSADO = 'REC', 'Recusado'
        EM_ANDAMENTO = 'AND', 'Em andamento'
        CONCLUIDO = 'CON', 'Concluído'
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    tipo = models.CharField(
        max_length=3,
        choices=TiposPedidos.choices,
        default=TiposPedidos.CONSOLE,
        verbose_name="Tipo de Pedido"
    )
    
    # NOVO CAMPO: Status do pedido
    status = models.CharField(
        max_length=3,
        choices=StatusPedido.choices,
        default=StatusPedido.PENDENTE,
        verbose_name="Status do Pedido"
    )
    
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
        ordering = ['-data_de_entrada'] # Ordena do mais novo para o mais antigo
    
    def __str__(self):
        return f"Pedido de {self.cliente.nome} ({self.get_tipo_display()})"
    
class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, verbose_name="Pedido", null=True, blank=True)
    mensagem = models.TextField(verbose_name="Mensagem")
    lida = models.BooleanField(default=False, verbose_name="Lida")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('INFO', 'Informação'),
            ('SUCESSO', 'Sucesso'),
            ('ALERTA', 'Alerta'),
            ('ERRO', 'Erro')
        ],
        default='INFO'
    )
    
    class Meta:
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Notificação para {self.usuario.username}"