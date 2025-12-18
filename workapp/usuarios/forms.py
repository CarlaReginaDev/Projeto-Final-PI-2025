# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cliente, Pedidos, Perfil

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ClienteRegistrationForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'cidade', 'estado', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Senha'
        })
    )

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        # Apenas campos que o cliente preenche, 'cliente' será preenchido na view
        fields = ['tipo', 'detalhes_orcamento']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}), # Usar Select para choices
            'detalhes_orcamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['cliente', 'tipo', 'detalhes_orcamento', 'valor_orcamento']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control', 'id': 'cliente'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'id': 'tipoServico'}),
            'detalhes_orcamento': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'id': 'descricao',
                'placeholder': 'Descreva o problema ou serviço necessário'
            }),
            'valor_orcamento': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'valor',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nome')
        self.fields['cliente'].label = "Cliente"
        self.fields['tipo'].label = "Tipo de Serviço"
        self.fields['detalhes_orcamento'].label = "Descrição do Serviço"
        self.fields['valor_orcamento'].label = "Valor (R$)"