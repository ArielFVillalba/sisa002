
from django.contrib import admin
from django.urls import path
from stock.views_inventario import *
from stock.views_inventario_lst  import *

urlpatterns = [
   path('inventario/<str:pk_token>/cargar/', inventario_cargar.as_view(), name='inventario_cargar'),
   path('inv_generarbase/', inv_generarbase, name='inv_generarbase'),
   path('inv_toma_login/', inv_toma_login, name='inv_toma_login'),
   path('inv_toma_empsuc/', inv_toma_empsuc, name='inv_toma_empsuc'),
   path('inv_toma_carga/', inv_toma_carga, name='inv_toma_carga'),
   path('cargarcodigo/', cargarcodigo, name='cargarcodigo'),
   path('inv_ajuste_cargar/', inv_ajuste_cargar, name='inv_ajuste_cargar'),
   path('inv_ajuste_procesar/', inv_ajuste_procesar, name='inv_ajuste_procesar'),
   path('views_inventario_lst/', views_inventario_lst, name='views_inventario_lst'),
   path('inv_inf_gral_listar/', inv_inf_gral_listar, name='inv_inf_gral_listar'),
   path('inv_inf_det_listar/', inv_inf_det_listar, name='inv_inf_det_listar'),

]
