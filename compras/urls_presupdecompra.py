
from django.contrib import admin
from django.urls import path
from compras.views_presupdecompra import *

urlpatterns = [
    path('presupuestocompcab_filtro/', presupuestocompcab_filtro, name='presupuestocompcab_filtro'),
    path('presupuestocompcab_filtro_lst/', presupuestocompcab_filtro_lst, name='presupuestocompcab_filtro_lst'),


    path('presupuestocompcab/<str:pk_token>/cargar/', presupuestocompcab_cargar.as_view(), name='presupuestocompcab_cargar'),
    path('presupuestocompcab/<str:cadena>/listar/', presupuestocompcab_listar, name='presupuestocompcab_listar'),
    path('presupuestocompcab/crear/', presupuestocompcab_crear.as_view(), name='presupuestocompcab_crear'),
    path('presupuestocompcab/<str:pk_token>/editar/', presupuestocompcab_editar.as_view(), name='presupuestocompcab_editar'),

    path('presupuestocompcab/<str:pk_token>/eliminar/', presupuestocompcab_eliminar.as_view(), name='presupuestocompcab_eliminar'),

    path('presupuestocompdet_listar/', presupuestocompdet_listar, name='presupuestocompdet_listar'),
    path('presupuestocompdet/<str:pk_token>/eliminar/', presupuestocompdet_eliminar, name='presupuestocompdet_eliminar'),
    path('presupuestocompdet_guardar/', presupuestocompdet_guardar, name='presupuestocompdet_guardar'),
    path('presupuestocompdet_editar/', presupuestocompdet_editar, name='presupuestocompdet_editar'),

]