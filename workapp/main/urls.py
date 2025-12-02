from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from usuarios import views  # Import views directly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('', views.login_view, name='home'),
    path('adicionar_pedido/', views.adicionar_pedido, name='adicionar_pedido'),
    # path('usuarios/', include('usuarios.urls')),  # Remove or keep both
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)