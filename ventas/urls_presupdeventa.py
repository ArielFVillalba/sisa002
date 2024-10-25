
from django.contrib import admin
from django.urls import path
from ventas.views_presupdeventa import *

urlpatterns = [
    path('presupuestoventacab_filtro/', presupuestoventacab_filtro, name='presupuestoventacab_filtro'),
    path('presupuestoventacab_filtro_lst/', presupuestoventacab_filtro_lst, name='presupuestoventacab_filtro_lst'),

    path('presupuestoventacab/<str:cadena>/listar/', presupuestoventacab_listar, name='presupuestoventacab_listar'),
    path('presupuestoventacab/<str:pk_token>/cargar/', presupuestoventacab_cargar.as_view(), name='presupuestoventacab_cargar'),
    path('presupuestoventacab/crear/', presupuestoventacab_crear.as_view(), name='presupuestoventacab_crear'),
    path('presupuestoventacab/<str:pk_token>/editar/', presupuestoventacab_editar.as_view(), name='presupuestoventacab_editar'),
    path('presupuestoventacab/<str:pk_token>/eliminar/', presupuestoventacab_eliminar.as_view(), name='presupuestoventacab_eliminar'),

    path('presupuestoventadet_listar/', presupuestoventadet_listar, name='presupuestoventadet_listar'),
    path('presupuestoventadet_guardar/', presupuestoventadet_guardar, name='presupuestoventadet_guardar'),
    path('presupuestoventadet_editar/', presupuestoventadet_editar, name='presupuestoventadet_editar'),
    path('presupuestoventadet/<str:pk_token>/eliminar/', presupuestoventadet_eliminar,name='presupuestoventadet_eliminar'),
]