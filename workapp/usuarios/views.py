# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ClienteRegistrationForm, UserRegistrationForm, LoginForm, PerfilForm, PedidosForm
from django.contrib.auth.models import User, Group
from .models import Cliente

def cadastrar_usuario(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        cliente_form = ClienteRegistrationForm(request.POST)
        
        if user_form.is_valid() and cliente_form.is_valid():
            # Create User first
            user = user_form.save()
            
            # Then create Cliente linked to the User
            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.save()
            
            # Add user to group
            grupo_simples, created = Group.objects.get_or_create(name='USUARIO_SIMPLES')
            user.groups.add(grupo_simples)
            
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        cliente_form = ClienteRegistrationForm()
    
    return render(request, 'usuarios/cadastrar.html', {
        'user_form': user_form,
        'cliente_form': cliente_form
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('perfil')  # If already logged in, go to profile
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')
                return redirect('perfil')  # Or wherever you want after login
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('login')

@login_required
def perfil_view(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        cliente = None
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=cliente)
    
    return render(request, 'usuarios/perfil.html', {'form': form})

@login_required
def adicionar_pedido(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'Erro: Dados do cliente não encontrados.')
        return redirect('perfil')
        
    if request.method == 'POST':
        form = PedidosForm(request.POST) # Use PedidosForm, não ConsolesForm (como no snippet anterior)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente  # 🌟 MUDANÇA CRÍTICA: Liga o pedido ao cliente
            pedido.save()
            messages.success(request, 'Pedido de conserto enviado com sucesso!')
            return redirect('perfil')
    else:
        form = PedidosForm()
    
    return render(request, 'usuarios/adicionar_pedido.html', {'form': form})