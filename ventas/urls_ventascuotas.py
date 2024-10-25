from ventas.views_ventascuotas import *
from django.urls import path

urlpatterns = [
     path('ventascuotas/<str:pk_token>/cargar/', ventascuotas_cargar, name='ventascuotas_cargar'),
     path('ventascuotas_generar/', ventascuotas_generar, name='ventascuotas_generar'),
     path('ventascuotas_listar/', ventascuotas_listar, name='ventascuotas_listar'),
     path('ventascuotas/<str:pk_token>/eliminar/', ventascuotas_eliminar, name='ventascuotas_eliminar'),
     path('ventascuotas/<str:pk_token>/eliminar/',ventascuotas_eliminar, name='ventascuotas_eliminar'),
     path('ventascuotas_mod/', ventascuotas_mod, name='ventascuotas_mod'),
     path('ventascuotas_guardar/', ventascuotas_guardar, name='ventascuotas_guardar'),

]