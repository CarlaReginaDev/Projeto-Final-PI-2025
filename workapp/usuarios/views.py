# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .forms import ClienteRegistrationForm, UserRegistrationForm, LoginForm, PedidosForm, PerfilForm
from django.contrib.auth.models import User, Group
from .models import Cliente, Pedidos, Notificacao
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date, timedelta
from django.db.models import Count, Sum
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
        # Tente pegar o cliente, mas se falhar, não quebre
        cliente = Cliente.objects.get(user=request.user)
    except (Cliente.DoesNotExist, Exception):
        # Se não existir ou se houver erro de banco, use None
        cliente = None
    
    if request.method == 'POST':
        # Use apenas dados do User para o form
        form = PerfilForm(request.POST)
        if form.is_valid():
            # Atualize o User, não o Cliente
            user = request.user
            user.first_name = form.cleaned_data.get('nome', '')
            user.email = form.cleaned_data.get('email', '')
            user.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        # Dados iniciais do User
        initial_data = {
            'nome': request.user.first_name or request.user.username,
            'email': request.user.email
        }
        form = PerfilForm(initial=initial_data)
    
    context = {
        'form': form,
        'cliente': cliente,  # Pode ser None
    }

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

@login_required
def registro_consoles(request):
    # Buscar clientes
    clientes = Cliente.objects.all().order_by('nome')
    
    # Buscar serviços do tipo Console
    servicos_consoles = Pedidos.objects.filter(tipo='CON').order_by('-data_de_entrada')
    
    # Contar totais
    total_servicos = servicos_consoles.count()
    servicos_aguardando = servicos_consoles.filter(status='PEN').count()
    servicos_andamento = servicos_consoles.filter(status='AND').count()
    servicos_concluidos = servicos_consoles.filter(status='CON').count()
    
    # Calcular valor total
    valor_total = servicos_consoles.aggregate(
        total=Sum('valor_orcamento')
    )['total'] or 0
    
    context = {
        'page_title': 'Serviços - Consoles',
        'hoje': date.today().isoformat(),
        'clientes': clientes,
        'servicos': servicos_consoles,
        'total_servicos': total_servicos,
        'servicos_aguardando': servicos_aguardando,
        'servicos_andamento': servicos_andamento,
        'servicos_concluidos': servicos_concluidos,
        'valor_total': valor_total,
    }
    return render(request, 'usuarios/registro_consoles.html', context)

@login_required
def registro_controles(request):
    # Buscar clientes
    clientes = Cliente.objects.all().order_by('nome')
    
    # Buscar serviços do tipo Controle
    servicos_controles = Pedidos.objects.filter(tipo='CTR').order_by('-data_de_entrada')
    
    # Contar totais
    total_servicos = servicos_controles.count()
    servicos_aguardando = servicos_controles.filter(status='PEN').count()
    servicos_andamento = servicos_controles.filter(status='AND').count()
    servicos_concluidos = servicos_controles.filter(status='CON').count()
    
    # Calcular valor total
    valor_total = servicos_controles.aggregate(
        total=Sum('valor_orcamento')
    )['total'] or 0
    
    context = {
        'page_title': 'Serviços - Controles',
        'hoje': date.today().isoformat(),
        'clientes': clientes,
        'servicos': servicos_controles,
        'total_servicos': total_servicos,
        'servicos_aguardando': servicos_aguardando,
        'servicos_andamento': servicos_andamento,
        'servicos_concluidos': servicos_concluidos,
        'valor_total': valor_total,
    }
    return render(request, 'usuarios/registro_controles.html', context)

@login_required
def registro_outros(request):
    # Buscar clientes
    clientes = Cliente.objects.all().order_by('nome')
    
    # Buscar serviços do tipo Outros
    servicos_outros = Pedidos.objects.filter(tipo='OUT').order_by('-data_de_entrada')
    
    # Contar totais
    total_servicos = servicos_outros.count()
    servicos_aguardando = servicos_outros.filter(status='PEN').count()
    servicos_andamento = servicos_outros.filter(status='AND').count()
    servicos_concluidos = servicos_outros.filter(status='CON').count()
    
    # Calcular valor total
    valor_total = servicos_outros.aggregate(
        total=Sum('valor_orcamento')
    )['total'] or 0
    
    context = {
        'page_title': 'Serviços - Outros',
        'hoje': date.today().isoformat(),
        'clientes': clientes,
        'servicos': servicos_outros,
        'total_servicos': total_servicos,
        'servicos_aguardando': servicos_aguardando,
        'servicos_andamento': servicos_andamento,
        'servicos_concluidos': servicos_concluidos,
        'valor_total': valor_total,
    }
    return render(request, 'usuarios/registro_outros.html', context)

@login_required
def clientes(request):
    # Buscar todos os clientes
    todos_clientes = Cliente.objects.all().order_by('nome')
    
    # Contar total de clientes
    total_clientes = todos_clientes.count()
    
    # Contar pedidos por cliente (opcional)
    clientes_com_pedidos = []
    for cliente in todos_clientes:
        pedidos_count = Pedidos.objects.filter(cliente=cliente).count()
        clientes_com_pedidos.append({
            'cliente': cliente,
            'total_pedidos': pedidos_count
        })
    
    context = {
        'page_title': 'Clientes',
        'hoje': date.today().isoformat(),
        'clientes': todos_clientes,
        'total_clientes': total_clientes,
        'clientes_com_pedidos': clientes_com_pedidos,
    }
    return render(request, 'clientes.html', context)

@login_required
def salvar_cliente(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            telefone = request.POST.get('telefone')
            cidade = request.POST.get('cidade', '')
            estado = request.POST.get('estado', '')
            data_cadastro = request.POST.get('data_cadastro')
            descricao = request.POST.get('descricao', '')
            
            # Validação
            if not nome or not telefone:
                messages.error(request, 'Nome e telefone são obrigatórios.')
                return redirect('clientes')
            
            # Verificar se telefone já existe
            if Cliente.objects.filter(telefone=telefone).exists():
                messages.error(request, 'Já existe um cliente com este telefone.')
                return redirect('clientes')
            
            # Processar data
            from datetime import datetime
            if data_cadastro:
                try:
                    data_obj = datetime.strptime(data_cadastro, '%Y-%m-%d').date()
                except:
                    data_obj = datetime.now().date()
            else:
                data_obj = datetime.now().date()
            
            # Criar endereço
            endereco = ""
            if cidade or estado:
                endereco = f"{cidade}{'/' if cidade and estado else ''}{estado}"
            
            # CRIAR CLIENTE VINCULADO AO USUÁRIO LOGADO
            cliente = Cliente.objects.create(
                user=request.user,  # VINCULE AO USUÁRIO LOGADO
                nome=nome,
                telefone=telefone,
                cidade=cidade,
                estado=estado,
                descricao=descricao,
                data_cadastro=data_obj
            )
            
            messages.success(request, f'Cliente "{nome}" salvo com sucesso!')
            return redirect('clientes')
            
        except Exception as e:
            messages.error(request, f'Erro ao salvar cliente: {str(e)}')
            return redirect('clientes')
    
    return redirect('clientes')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def salvar_servico_console(request):
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            descricao = request.POST.get('descricao')
            valor = request.POST.get('valor')
            
            # Validação
            if not cliente_id or not descricao or not valor:
                messages.error(request, 'Todos os campos são obrigatórios.')
                return redirect('registro_consoles')
            
            cliente = Cliente.objects.get(telefone=cliente_id)
            
            # Criar pedido
            Pedidos.objects.create(
                cliente=cliente,
                tipo='CON',
                detalhes_orcamento=descricao,
                valor_orcamento=valor,
                status='PEN'
            )
            
            messages.success(request, 'Serviço de console registrado com sucesso!')
            return redirect('registro_consoles')
            
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
            return redirect('registro_consoles')
    
    return redirect('registro_consoles')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def salvar_servico_controle(request):
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            descricao = request.POST.get('descricao')
            valor = request.POST.get('valor')
            
            if not cliente_id or not descricao or not valor:
                messages.error(request, 'Todos os campos são obrigatórios.')
                return redirect('registro_controles')
            
            cliente = Cliente.objects.get(telefone=cliente_id)
            
            Pedidos.objects.create(
                cliente=cliente,
                tipo='CTR',
                detalhes_orcamento=descricao,
                valor_orcamento=valor,
                status='PEN'
            )
            
            messages.success(request, 'Serviço de controle registrado com sucesso!')
            return redirect('registro_controles')
            
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
            return redirect('registro_controles')
    
    return redirect('registro_controles')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def salvar_servico_outros(request):
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            descricao = request.POST.get('descricao')
            valor = request.POST.get('valor')
            
            if not cliente_id or not descricao or not valor:
                messages.error(request, 'Todos os campos são obrigatórios.')
                return redirect('registro_outros')
            
            cliente = Cliente.objects.get(telefone=cliente_id)
            
            Pedidos.objects.create(
                cliente=cliente,
                tipo='OUT',
                detalhes_orcamento=descricao,
                valor_orcamento=valor,
                status='PEN'
            )
            
            messages.success(request, 'Serviço registrado com sucesso!')
            return redirect('registro_outros')
            
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
            return redirect('registro_outros')
    
    return redirect('registro_outros')