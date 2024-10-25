
from django.contrib import admin
from django.urls import path
from ventas.views_notacreditodeventa import *

urlpatterns = [

    path('notacreditoventacab_filtro/',notacreditoventacab_filtro, name='notacreditoventacab_filtro'),
    path('notacreditoventacab_filtro_lst/',notacreditoventacab_filtro_lst, name='notacreditoventacab_filtro_lst'),


    path('notacreditoventacab/<str:cadena>/listar/', notacreditoventacab_listar, name='notacreditoventacab_listar'),
    path('notacreditoventacab/<str:pk_token>/cargar/', notacreditoventacab_cargar.as_view(), name='notacreditoventacab_cargar'),
    path('notacreditoventacab/crear/', notacreditoventacab_crear.as_view(), name='notacreditoventacab_crear'),
    path('notacreditoventacab/<str:pk_token>/editar/', notacreditoventacab_editar.as_view(), name='notacreditoventacab_editar'),
    path('notacreditoventacab/<str:pk_token>/eliminar/', notacreditoventacab_eliminar.as_view(),name='notacreditoventacab_eliminar'),

    path('notacreditoventadet_listar/', notacreditoventadet_listar, name='notacreditoventadet_listar'),
    path('notacreditoventadet_guardar/',notacreditoventadet_guardar, name='notacreditoventadet_guardar'),
    path('notacreditoventadet_editar/', notacreditoventadet_editar, name='notacreditoventadet_editar'),
    path('notacreditoventadet/<str:pk_token>/eliminar/', notacreditoventadet_eliminar,name='notacreditoventadet_eliminar'),

]