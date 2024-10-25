
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *

from compras.views_compra import *
from compras.views_pagoprov import *

urlpatterns = [

    path('pagoprovcab_filtro/',pagoprovcab_filtro, name='pagoprovcab_filtro'),
    path('pagoprovcab_filtro_lst/', pagoprovcab_filtro_lst, name='pagoprovcab_filtro_lst'),
    path('pagoprovcab/<str:cadena>/listar/',pagoprovcab_listar, name='pagoprovcab_listar'),
    path('pagoprovcab/<str:pk_token>/cargar/', pagoprovcab_cargar.as_view(), name='pagoprovcab_cargar'),
    path('pagoprovcab/crear/', pagoprovcab_crear.as_view(), name='pagoprovcab_crear'),
    path('pagoprovcab/<str:pk_token>/editar/', pagoprovcab_editar.as_view(), name='pagoprovcab_editar'),
    path('pagoprovcab/<str:pk_token>/eliminar/', pagoprovcab_eliminar.as_view(), name='pagoprovcab_eliminar'),
    path('pagoprovfact/<str:pk_token1>/<str:pk_token2>/agregar/', pagoprovfact_agregar.as_view(), name='pagoprovfact_agregar'),
    path('pagoprovafact/<str:pk_token>/listar/', pagoprovafact_listar.as_view(), name='pagoprovafact_listar'),
    path('pagoprovfact_listar/', pagoprovfact_listar, name='pagoprovfact_listar'),
    path('pagoprovfact_editar/', pagoprovfact_editar, name='pagoprovfact_editar'),
    path('pagoprovfact/<str:pk_token>/eliminar/', pagoprovfact_eliminar.as_view(), name='pagoprovfact_eliminar'),
    path('pagoprovpago_listar/', pagoprovpago_listar, name='pagoprovpago_listar'),
    path('pagoprovpago_agregar/', pagoprovpago_agregar, name='pagoprovpago_agregar'),
    path('pagoprovpago/<str:pk_token>/eliminar/', pagoprovpago_eliminar.as_view(), name='pagoprovpago_eliminar'),

    #path('compradet_listar/', compradet_listar, name='compradet_listar'),
    #path('compradet/<str:pk_token>/eliminar/', compradet_eliminar, name='compradet_eliminar'),
    #path('guardardet/', guardardet, name='guardardet'),
    #path('compradetmod/', compradetmod, name='compradetmod'),

]