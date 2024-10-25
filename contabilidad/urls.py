
from django.contrib import admin
from django.urls import path, include
from contabilidad import views
from contabilidad.views import *
from contabilidad.views_cuenta_contable import *


urlpatterns = [
    path('', include('contabilidad.urls_asiento')),
    path('menucontabilidad/', views.menucontabilidad, name="menucontabilidad"),
    path('ctacontable/<str:pk_token>/cargar/', ctacontable_cargar.as_view(), name='ctacontable_cargar'),
    path('ctacontable/crear/', ctacontable_crear.as_view(), name='ctacontable_crear'),
    path('ctacontable/<str:pk_token>/editar/', ctacontable_editar.as_view(), name='ctacontable_editar'),
    path('ctacontable/<str:pk_token>/eliminar/', ctacontable_eliminar.as_view(), name='ctacontable_eliminar'),
    path('ctacontable/<str:cadena>/listar/', ctacontable_listar, name='ctacontable_listar'),
    path('ctacontable_filtar/', ctacontable_filtar, name='ctacontable_filtar'),
    path('ctacontable/<str:cadena>/listar/', ctacontable_listar, name='ctacontable_listar'),
    path('librodiario/<str:cadena>/listar/', librodiario_listar, name='librodiario_listar'),
    path('libro_diario_filtrar_lst/', libro_diario_filtrar_lst, name='libro_diario_filtrar_lst'),
    path('libro_diario_filtrar/', libro_diario_filtrar, name='libro_diario_filtrar'),

]