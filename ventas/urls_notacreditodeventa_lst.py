
from django.contrib import admin
from django.urls import path
from ventas import views
from ventas.views import *

from ventas.views_notacreditodeventa_lst import *

urlpatterns = [
    path('notacreditodeventacab_inf/', notacreditodeventacab_inf, name='notacreditodeventacab_inf'),
    path('notacreditodeventacabinf_listar/', notacreditodeventacabinf_listar, name='notacreditodeventacabinf_listar'),
    path('notacreditodeventacabinfpdf/', notacreditodeventacabinfpdf, name="notacreditodeventacabinfpdf"),
    path('notacreditodeventacabinfexcel/', notacreditodeventacabinfexcel, name="notacreditodeventacabinfexcel"),
    path('notacreditodeventacabinfcsv/', notacreditodeventacabinfcsv, name="notacreditodeventacabinfcsv"),

    path('notacreditodeventadetinf_listar/', notacreditodeventadetinf_listar, name='notacreditodeventadetinf_listar'),
    path('notacreditodeventadetinfpdf/', notacreditodeventadetinfpdf, name="notacreditodeventadetinfpdf"),
    path('notacreditodeventadetinfexcel/', notacreditodeventadetinfexcel, name="notacreditodeventadetinfexcel"),
    path('notacreditodeventadetinfcsv/', notacreditodeventadetinfcsv, name="notacreditodeventadetinfcsv"),
    
]