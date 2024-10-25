
from django.contrib import admin
from django.urls import path
from compras.views_pedidodecompra import *

urlpatterns = [

    path('pedidocompcab_filtro/', pedidocompcab_filtro, name='pedidocompcab_filtro'),
    path('pedidocompcab_filtro_lst/', pedidocompcab_filtro_lst, name='pedidocompcab_filtro_lst'),

    path('pedidocompcab/<str:cadena>/listar/', pedidocompcab_listar, name='pedidocompcab_listar'),
    path('pedidocompcab/<str:pk_token>/cargar/', pedidocompcab_cargar.as_view(), name='pedidocompcab_cargar'),


    path('pedidocompcab/crear/', pedidocompcab_crear.as_view(), name='pedidocompcab_crear'),
    path('pedidocompcab/<str:pk_token>/editar/', pedidocompcab_editar.as_view(), name='pedidocompcab_editar'),
    path('pedidocompcab/<str:pk_token>/eliminar/', pedidocompcab_eliminar.as_view(), name='pedidocompcab_eliminar'),

    path('pedidocompdet_listar/', pedidocompdet_listar, name='pedidocompdet_listar'),
    path('pedidocompdet/<str:pk_token>/eliminar/', pedidocompdet_eliminar, name='pedidocompdet_eliminar'),
    path('pedidocompdet_guardar/', pedidocompdet_guardar, name='pedidocompdet_guardar'),
    path('pedidocompdet_editar/', pedidocompdet_editar, name='pedidocompdet_editar'),

]