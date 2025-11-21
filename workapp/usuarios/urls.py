# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('adicionar_pedido/', views.adicionar_pedido, name='adicionar_pedido'),
    path('', views.login_view, name='home'),
]