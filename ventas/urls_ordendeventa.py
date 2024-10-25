
from django.contrib import admin
from django.urls import path
from ventas.views_ordendeventa import *

urlpatterns = [
    path('ordenventacab_filtro/', ordenventacab_filtro, name='ordenventacab_filtro'),
    path('ordenventacab_filtro_lst/', ordenventacab_filtro_lst, name='ordenventacab_filtro_lst'),
    path('ordenventacab/<str:pk_token>/cargar/', ordenventacab_cargar.as_view(), name='ordenventacab_cargar'),
    path('ordenventacab/<str:cadena>/listar/', ordenventacab_listar, name='ordenventacab_listar'),
    path('ordenventacab/crear/', ordenventacab_crear.as_view(), name='ordenventacab_crear'),
    path('ordenventacab/<str:pk_token>/editar/', ordenventacab_editar.as_view(), name='ordenventacab_editar'),
    path('ordenventacab/<str:pk_token>/eliminar/', ordenventacab_eliminar.as_view(), name='ordenventacab_eliminar'),
    path('ordenventadet_listar/', ordenventadet_listar, name='ordenventadet_listar'),
    path('ordenventadet_guardar/', ordenventadet_guardar, name='ordenventadetguardar'),
    path('ordenventadet_editar/', ordenventadet_editar, name='ordenventadetmod'),
    path('ordenventadet/<str:pk_token>/eliminar/', ordenventadet_eliminar, name='ordenventadet_eliminar'),

]