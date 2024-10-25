
from django.urls import path
from ventas.views_pagocli import *

urlpatterns = [

    path('pagoclicab_filtro/',pagoclicab_filtro, name='pagoclicab_filtro'),
    path('pagoclicab_filtro_lst/', pagoclicab_filtro_lst, name='pagoclicab_filtro_lst'),
    path('pagoclicab/<str:cadena>/listar/',pagoclicab_listar, name='pagoclicab_listar'),
    path('pagoclicab/<str:pk_token>/cargar/', pagoclicab_cargar.as_view(), name='pagoclicab_cargar'),
    path('pagoclicab/crear/', pagoclicab_crear.as_view(), name='pagoclicab_crear'),
    path('pagoclicab/<str:pk_token>/editar/', pagoclicab_editar.as_view(), name='pagoclicab_editar'),
    path('pagoclicab/<str:pk_token>/eliminar/', pagopclicab_eliminar.as_view(), name='pagoclicab_eliminar'),
    path('pagoclifact/<str:pk_token1>/<str:pk_token2>/agregar/', pagoclifact_agregar.as_view(), name='pagoclifact_agregar'),
    path('pagocliafact/<str:pk_token>/listar/', pagocliafact_listar.as_view(), name='pagocliafact_listar'),
    path('pagoclifact_listar/', pagoclifact_listar, name='pagoclifact_listar'),
    path('pagoclifact_editar/', pagoclifact_editar, name='pagoclifact_editar'),
    path('pagoclifact/<str:pk_token>/eliminar/', pagoclifact_eliminar.as_view(), name='pagoclifact_eliminar'),
    path('pagoclipago_listar/', pagoclipago_listar, name='pagoclipago_listar'),
    path('pagoclipago_agregar/', pagoclipago_agregar, name='pagoclipago_agregar'),
    path('pagoclipago/<str:pk_token>/eliminar/', pagoclipago_eliminar.as_view(), name='pagoclipago_eliminar'),

    #path('compradet_listar/', compradet_listar, name='compradet_listar'),
    #path('compradet/<str:pk_token>/eliminar/', compradet_eliminar, name='compradet_eliminar'),
    #path('guardardet/', guardardet, name='guardardet'),
    #path('compradetmod/', compradetmod, name='compradetmod'),

]