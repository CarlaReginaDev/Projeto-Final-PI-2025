# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .forms import ClienteRegistrationForm, UserRegistrationForm, LoginForm, PerfilForm, PedidosForm
from django.contrib.auth.models import User, Group
from .models import Cliente, Pedidos, Notificacao
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def gerenciar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedidos, id=pedido_id)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        mensagem = request.POST.get('mensagem_admin', '')
        
        if novo_status in dict(Pedidos.StatusPedido.choices):
            pedido.status = novo_status
            pedido.mensagem_admin = mensagem
            pedido.save()
            
            # Cria notificação
            Notificacao.objects.create(
                usuario=pedido.cliente.user,
                pedido=pedido,
                mensagem=f"Seu pedido #{pedido.id} foi atualizado: {pedido.get_status_display()}. {mensagem}",
                tipo='INFO' if novo_status == 'PEN' else 'SUCESSO' if novo_status == 'ACE' else 'ALERTA'
            )
            
            messages.success(request, f'Pedido #{pedido.id} atualizado com sucesso!')
            return redirect('listar_pedidos')
    
    return render(request, 'usuarios/gerenciar_pedido.html', {'pedido': pedido})

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def atualizar_valor_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedidos, id=pedido_id)
    
    if request.method == 'POST':
        valor = request.POST.get('valor_orcamento')
        if valor:
            pedido.valor_orcamento = valor
            pedido.status = Pedidos.StatusPedido.ACEITO
            pedido.save()
            
            Notificacao.objects.create(
                usuario=pedido.cliente.user,
                pedido=pedido,
                mensagem=f"Orçamento para seu pedido #{pedido.id}: R$ {valor}. Pedido ACEITO!",
                tipo='SUCESSO'
            )
            
            messages.success(request, f'Valor do pedido #{pedido.id} atualizado!')
    
    return redirect('gerenciar_pedido', pedido_id=pedido_id)

@login_required
def notificacoes_view(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-data_criacao')
    
    # Marcar como lidas quando visualizadas
    notificacoes_nao_lidas = notificacoes.filter(lida=False)
    notificacoes_nao_lidas.update(lida=True)
    
    return render(request, 'usuarios/notificacoes.html', {'notificacoes': notificacoes})

@login_required
def contar_notificacoes_nao_lidas(request):
    count = Notificacao.objects.filter(usuario=request.user, lida=False).count()
    return {'notificacoes_nao_lidas': count}

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
        form = PedidosForm(request.POST) 
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = cliente  
            pedido.save()
            messages.success(request, 'Pedido de conserto enviado com sucesso!')
            return redirect('perfil')
    else:
        form = PedidosForm()
    
    return render(request, 'usuarios/adicionar_pedido.html', {'form': form})

def is_admin_or_staff(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/perfil/') 
def listar_pedidos(request):
    todos_pedidos = Pedidos.objects.all().order_by('-data_de_entrada') # 👈 Obtém todos
    paginator = Paginator(todos_pedidos, 10) # 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'usuarios/listar_pedidos.html', {'page_obj': page_obj})

@login_required
def dashboard(request):
    return render(request, 'usuarios/dashboard.html')