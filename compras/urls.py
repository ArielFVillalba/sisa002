
from django.contrib import admin
from django.urls import path, include
from compras import views
from compras.views import *
from stock.views_articulos import *
from compras.views_proveedor import *
from compras.views_compra import *


urlpatterns = [
    path('', include('compras.urls_compra')),
    path('', include('compras.urls_comprascuotas')),
    path('', include('compras.urls_compra_lst')),
    path('', include('compras.urls_pagoprov')),
    path('', include('compras.urls_ordendecompra')),
    path('', include('compras.urls_ordendecompra_lst')),
    path('', include('compras.urls_pedidodecompra')),
    path('', include('compras.urls_pedidodecompra_lst')),
    path('', include('compras.urls_presupdecompra')),
    path('', include('compras.urls_presupdecompra_lst')),
    path('', include('compras.urls_notacreditodecompra')),
    path('', include('compras.urls_notacreditodecompra_lst')),
    path('', include('compras.urls_notadebitodecompra')),
    path('', include('compras.urls_notadebitodecompra_lst')),

    #path('', include('compras.urls_pdf')),

    path('menucompras/', views.menucompras, name="menucompras"),
    path('menuproveedor/', views.menuproveedor, name="menuproveedor"),
    path('proveedor/<str:cadena>/listar/', proveedor_listar, name='proveedor_listar'),
    path('proveedor/<str:pk_token>/cargar/', proveedor_cargar.as_view(), name='proveedor_cargar'),
    path('proveedor/crear/', proveedor_crear.as_view(), name='proveedor_crear'),
    path('proveedor/<str:pk_token>/editar/', proveedor_editar.as_view(), name='proveedor_editar'),
    path('proveedor/<str:pk_token>/eliminar/', proveedor_eliminar.as_view(), name='proveedor_eliminar'),
    path('proveedor2/<str:pk_token>/eliminar/', proveedor2_eliminar, name='proveedor2_eliminar'),
    path('cmbprov/', cmbprov, name="cmbprov"),
    path('prov_datos/', prov_datos, name="prov_datos"),


]