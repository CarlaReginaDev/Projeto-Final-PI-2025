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

class Consoles(models.Model):
    nome_cliente = models.CharField(max_length=150, verbose_name="Nome do cliente")
    tipo_console = models.CharField(max_length=100, verbose_name="Tipo de Console")
    data_de_entrada = models.DateField(verbose_name="Data de Entrada")
    detalhes_orcamento = models.ForeignKey(Login_Usuario, verbose_name="Detalhes do Orçamento", on_delete=models.CASCADE)
    valor_orcamento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Orçamento")
    data_saida = models.DateField(null=True, blank=True, verbose_name="Data de Saída")
    
    class Meta:
        app_label = 'usuarios'
    
    def __str__(self):
        return f"{self.nome_cliente} - {self.tipo_console}"

class Controles(models.Model):
    nome_cliente = models.CharField(max_length=150, verbose_name="Nome do cliente")
    tipo_controle = models.CharField(max_length=100, verbose_name="Tipo de Controle")
    data_de_entrada = models.DateField(auto_now_add=True, verbose_name="Data de Entrada")
    detalhes_orcamento = models.ForeignKey(Login_Usuario, verbose_name="Detalhes do Orçamento", on_delete=models.CASCADE)
    valor_orcamento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Orçamento")
    data_saida = models.DateField(null=True, blank=True, verbose_name="Data de Saída")
    
    class Meta:
        app_label = 'usuarios'
    
    def __str__(self):
        return f"{self.nome_cliente} - {self.tipo_controle}"

class Outros(models.Model):
    nome_cliente = models.CharField(max_length=150, verbose_name="Nome do cliente")
    tipo_outro = models.CharField(max_length=100, verbose_name="Acessórios/Outros")
    data_de_entrada = models.DateField(auto_now_add=True, verbose_name="Data de Entrada")
    detalhes_orcamento = models.ForeignKey(Login_Usuario, verbose_name="Detalhes do Orçamento", on_delete=models.CASCADE)
    valor_orcamento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Orçamento")
    data_saida = models.DateField(null=True, blank=True, verbose_name="Data de Saída")
    
    class Meta:
        app_label = 'usuarios'
    
    def __str__(self):
        return f"{self.nome_cliente} - {self.tipo_outro}"