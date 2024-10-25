
from django.contrib import admin
from django.urls import path
from compras.views_notadebitodecompra import *

urlpatterns = [

    path('notadebitocompcab_filtro/',notadebitocompcab_filtro, name='notadebitocompcab_filtro'),
    path('notadebitocompcab_filtro_lst/',notadebitocompcab_filtro_lst, name='notadebitocompcab_filtro_lst'),

    path('notadebitocompcab/<str:cadena>/listar/', notadebitocompcab_listar, name='notadebitocompcab_listar'),
    path('notadebitocompcab/<str:pk_token>/cargar/', notadebitocompcab_cargar.as_view(), name='notadebitocompcab_cargar'),
    path('notadebitocompcab/crear/', notadebitocompcab_crear.as_view(), name='notadebitocompcab_crear'),
    path('notadebitocompcab/<str:pk_token>/editar/', notadebitocompcab_editar.as_view(), name='notadebitocompcab_editar'),
    path('notadebitocompcab/<str:pk_token>/eliminar/', notadebitocompcab_eliminar.as_view(), name='notadebitocompcab_eliminar'),

    path('notadebitocompdet_listar/', notadebitocompdet_listar, name='notadebitocompdet_listar'),
    path('notadebitocompdet/<str:pk_token>/eliminar/', notadebitocompdet_eliminar, name='notadebitocompdet_eliminar'),
    path('notadebitocompdet_guardar/', notadebitocompdet_guardar, name='notadebitocompdet_guardar'),
    path('notadebitocompdet_editar/', notadebitocompdet_editar, name='notadebitocompdet_editar'),

]