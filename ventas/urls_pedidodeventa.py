
from django.contrib import admin
from django.urls import path
from ventas.views_pedidodeventa import *

urlpatterns = [

    path('pedidoventacab_filtro/', pedidoventacab_filtro, name='pedidoventacab_filtro'),
    path('pedidoventacab_filtro_lst/', pedidoventacab_filtro_lst, name='pedidoventacab_filtro_lst'),
    path('pedidoventacab/<str:pk_token>/cargar/', pedidoventacab_cargar.as_view(), name='pedidoventacab_cargar'),
    path('pedidoventacab/crear/', pedidoventacab_crear.as_view(), name='pedidoventacab_crear'),
    path('pedidoventacab/<str:pk_token>/editar/', pedidoventacab_editar.as_view(),name='pedidoventacab_editar'),
    path('pedidoventacab/<str:pk_token>/eliminar/', pedidoventacab_eliminar.as_view(), name='pedidoventacab_eliminar'),
    path('pedidoventadet_listar/', pedidoventadet_listar, name='pedidoventadet_listar'),
    path('pedidoventadet_guardar/', pedidoventadet_guardar, name='pedidoventadet_guardar'),
    path('pedidoventadet_editar/', pedidoventadet_editar, name='pedidoventadet_editar'),
    path('pedidoventadet/<str:pk_token>/eliminar/', pedidoventadet_eliminar, name='pedidoventadet_eliminar'),

]