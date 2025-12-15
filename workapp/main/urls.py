from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('', views.login_view, name='home'),
    path('adicionar_pedido/', views.adicionar_pedido, name='adicionar_pedido'),
    path('pedidos/gerenciar/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/gerenciar/<int:pedido_id>/', views.gerenciar_pedido, name='gerenciar_pedido'),
    path('pedidos/atualizar-valor/<int:pedido_id>/', views.atualizar_valor_pedido, name='atualizar_valor_pedido'),
    path('notificacoes/', views.notificacoes_view, name='notificacoes'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)