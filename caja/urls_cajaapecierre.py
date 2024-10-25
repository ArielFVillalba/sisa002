

from django.contrib import admin
from django.urls import path
from caja.views_cajaapcierre import *
urlpatterns = [
    path('cajaapertura/', cajaapertura, name='cajaapertura'),
    path('cajaapertura_cargar/', cajaapertura_cargar.as_view(), name='cajaapertura_cargar'),
    path('cajaapertura_guardar/', cajaapertura_guardar, name='cajaapertura_guardar'),
    path('cajaaperturacierre/',cajaaperturacierre, name='cajaaperturacierre'),
    path('cajaapcierre/<str:pk_token>/cerrar/', cajaapcierre_cerrar, name='cajaapcierre_cerrar'),
    path('cajaapcierre/<str:pk_token>/cargar/', cajaapcierre_cargar.as_view(), name='cajaapcierre_cargar'),
    path('cajaapcierredet_listar/', cajaapcierredet_listar, name="cajaapcierredet_listar"),
    path('cajaapcierredet_guardar/', cajaapcierredet_guardar, name="cajaapcierredet_guardar"),
    path('cajaapcierredet/<str:pk_token>/eliminar/', cajaapcierredet_eliminar, name='cajaapcierredet_eliminar'),
]