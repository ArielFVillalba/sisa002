from compras.views_comprascuotas import *
from django.urls import path

urlpatterns = [
     path('comprascuotas/<str:pk_token>/cargar/', comprascuotas_cargar, name='comprascuotas_cargar'),
     path('comprascuotas_generar/', comprascuotas_generar, name='comprascuotas_generar'),
     path('comprascuotas_listar/', comprascuotas_listar, name='comprascuotas_listar'),
     path('comprascuotas/<str:pk_token>/eliminar/', comprascuotas_eliminar, name='comprascuotas_eliminar'),
     path('comprascuotas/<str:pk_token>/eliminar/', comprascuotas_eliminar, name='comprascuotas_eliminar'),
     path('comprascuotas_mod/', comprascuotas_mod, name='comprascuotas_mod'),
     path('comprascuotas_guardar/', comprascuotas_guardar, name='comprascuotas_guardar'),

]