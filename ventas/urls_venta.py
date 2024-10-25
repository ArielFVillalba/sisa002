
from django.contrib import admin
from django.urls import path
from ventas import views
from ventas.views import *

from ventas.views_venta import *

urlpatterns = [

    path('ventaracab_filtro/',ventacab_filtro, name='ventacab_filtro'),
    path('ventacab_filtro_lst/', ventacab_filtro_lst, name='ventacab_filtro_lst'),


    path('ventacab/<str:cadena>/listar/', ventacab_listar, name='ventacab_listar'),
    path('ventacab/<str:pk_token>/cargar/', ventacab_cargar.as_view(), name='ventacab_cargar'),

    path('ventacab/crear/', ventacab_crear.as_view(), name='ventacab_crear'),
    path('ventacab/<str:pk_token>/editar/', ventacab_editar.as_view(), name='ventacab_editar'),
    path('ventacab/<str:pk_token>/eliminar/', ventacab_eliminar.as_view(), name='ventacab_eliminar'),

    path('ventadet_listar/', ventadet_listar, name='ventadet_listar'),
    path('ventadet/<str:pk_token>/eliminar/', ventadet_eliminar, name='ventadet_eliminar'),
    path('ventadet_guardar/', ventadet_guardar, name='ventadet_guardar'),
    path('ventadet_editar/', ventadet_editar, name='ventadet_editar'),

]