from django.urls import path
from . import views
from .views import *
from .views_usuario import *

app_name = 'usuario'
urlpatterns = [
        path('listado/', UsuarioListado.as_view(), name='Usuarios_listado'),
        path('crear/', Usuario_crear.as_view(), name='Usuarios_crear'),
        path('editar/<int:pk>/', UsuarioEditar.as_view(), name='Usuario_editar'),
        path('borrar/<int:pk>/', UsuarioBorrar.as_view(), name='Usuario_borrar'),
    # path('empleados/detalle/<int:pk>/', EmpleadosDetalle.as_view(), name='Empleados_detalle'),

]