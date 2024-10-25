
from django.contrib import admin
from django.urls import path
from compras.views_notacreditodecompra import *

urlpatterns = [

    path('notacreditocompcab_filtro/',notacreditocompcab_filtro, name='notacreditocompcab_filtro'),
    path('notacreditocompcab_filtro_lst/',notacreditocompcab_filtro_lst, name='notacreditocompcab_filtro_lst'),

    path('notacreditocompcab/<str:cadena>/listar/', notacreditocompcab_listar, name='notacreditocompcab_listar'),
    path('notacreditocompcab/<str:pk_token>/cargar/', notacreditocompcab_cargar.as_view(), name='notacreditocompcab_cargar'),
    path('notacreditocompcab/crear/', notacreditocompcab_crear.as_view(), name='notacreditocompcab_crear'),
    path('notacreditocompcab/<str:pk_token>/editar/', notacreditocompcab_editar.as_view(), name='notacreditocompcab_editar'),
    path('notacreditocompcab/<str:pk_token>/eliminar/', notacreditocompcab_eliminar.as_view(), name='notacreditocompcab_eliminar'),

    path('notacreditocompdet_listar/', notacreditocompdet_listar, name='notacreditocompdet_listar'),
    path('notacreditocompdet/<str:pk_token>/eliminar/', notacreditocompdet_eliminar, name='notacreditocompdet_eliminar'),
    path('notacreditocompdet_guardar/', notacreditocompdet_guardar, name='notacreditocompdetguardar'),
    path('notacreditocompdet_editar/', notacreditocompdet_editar, name='notacreditocompdetmod'),

]