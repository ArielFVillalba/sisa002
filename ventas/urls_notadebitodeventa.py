
from django.contrib import admin
from django.urls import path
from ventas.views_notadebitodeventa import *

urlpatterns = [

    path('notadebitoventacab_filtro/', notadebitoventacab_filtro, name='notadebitoventacab_filtro'),
    path('notadebitoventacab_filtro_lst/', notadebitoventacab_filtro_lst, name='notadebitoventacab_filtro_lst'),

    path('notadebitoventacab/<str:cadena>/listar/', notadebitoventacab_listar, name='notadebitoventacab_listar'),
    path('notadebitoventacab/<str:pk_token>/cargar/', notadebitoventacab_cargar.as_view(), name='notadebitoventacab_cargar'),
    path('notadebitoventacab/crear/', notadebitoventacab_crear.as_view(), name='notadebitoventacab_crear'),
    path('notadebitoventacab/<str:pk_token>/editar/', notadebitoventacab_editar.as_view(), name='notadebitoventacab_editar'),
    path('notadebitoventacab/<str:pk_token>/eliminar/',notadebitoventacab_eliminar.as_view(),name='notadebitoventacab_eliminar'),

    path('notadebitoventadet_listar/', notadebitoventadet_listar, name='notadebitoventadet_listar'),
    path('notadebitoventadet_guardar/',notadebitoventadet_guardar, name='notadebitoventadet_guardar'),
    path('notadebitoventadet_editar/', notadebitoventadet_editar, name='notadebitoventadet_editar'),
    path('notadebitoventadet/<str:pk_token>/eliminar/', notadebitoventadet_eliminar,name='notadebitoventadet_eliminar'),

]


