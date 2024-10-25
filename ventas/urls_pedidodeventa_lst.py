
from django.contrib import admin
from django.urls import path
from ventas import views
from ventas.views import *

from ventas.views_pedidodeventa_lst import *

urlpatterns = [
    path('pedidodeventacab_inf/', pedidodeventacab_inf, name='pedidodeventacab_inf'),
    path('pedidodeventacabinf_listar/', pedidodeventacabinf_listar, name='pedidodeventacabinf_listar'),
    path('pedidodeventacabinfpdf/', pedidodeventacabinfpdf, name="pedidodeventacabinfpdf"),
    path('pedidodeventacabinfexcel/', pedidodeventacabinfexcel, name="pedidodeventacabinfexcel"),
    path('pedidodeventacabinfcsv/', pedidodeventacabinfcsv, name="pedidodeventacabinfcsv"),

    path('pedidodeventadetinf_listar/', pedidodeventadetinf_listar, name='pedidodeventadetinf_listar'),
    path('pedidodeventadetinfpdf/', pedidodeventadetinfpdf, name="pedidodeventadetinfpdf"),
    path('pedidodeventadetinfexcel/', pedidodeventadetinfexcel, name="pedidodeventadetinfexcel"),
    path('pedidodeventadetinfcsv/', pedidodeventadetinfcsv, name="pedidodeventadetinfcsv"),
    
]