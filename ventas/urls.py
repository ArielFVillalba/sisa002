
from django.contrib import admin
from django.urls import path, include
from ventas import views
from ventas.views import *
from ventas.views_cliente import *
from ventas.views_venta import *


urlpatterns = [
    path('', include('ventas.urls_venta')),
    path('', include('ventas.urls_ventascuotas')),
    path('', include('ventas.urls_pagocli')),

    path('', include('ventas.urls_venta_lst')),
    path('', include('ventas.urls_ordendeventa')),
    path('', include('ventas.urls_ordendeventa_lst')),

    path('', include('ventas.urls_pedidodeventa')),
    path('', include('ventas.urls_pedidodeventa_lst')),

    path('', include('ventas.urls_presupdeventa')),
    path('', include('ventas.urls_presupdeventa_lst')),

    path('', include('ventas.urls_notacreditodeventa')),
    path('', include('ventas.urls_notacreditodeventa_lst')),

    path('', include('ventas.urls_notadebitodeventa')),
    path('', include('ventas.urls_notadebitodeventa_lst')),

    path('menuventas/', views.menuventas, name="menuventas"),
    path('menuc/', views.menuventas, name="menuventas"),
    path('menucliente/', views.menucliente, name="menucliente"),

    path('cliente/<str:cadena>/listar/', cliente_listar, name='cliente_listar'),
    path('cliente/<str:pk_token>/cargar/', cliente_cargar.as_view(), name='cliente_cargar'),
    path('cliente/crear/', cliente_crear.as_view(), name='cliente_crear'),
    path('cliente/<str:pk_token>/editar/', cliente_editar.as_view(), name='cliente_editar'),
    path('cliente/<str:pk_token>/eliminar/', cliente_eliminar.as_view(), name='cliente_eliminar'),

    path('cmbcli/', cmbcli, name="cmbcli"),
    path('cli_datos/', cli_datos, name="cli_datos"),
    path('cli_ci_ruc/', cli_ci_ruc, name="cli_ci_ruc"),

]