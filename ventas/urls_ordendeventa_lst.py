
from django.contrib import admin
from django.urls import path
from ventas import views
from ventas.views import *

from ventas.views_ordendeventa_lst import *

urlpatterns = [
    path('ordendeventacab_inf/', ordendeventacab_inf, name='ordendeventacab_inf'),
    path('ordendeventacabinf_listar/', ordendeventacabinf_listar, name='ordendeventacabinf_listar'),
    path('ordendeventacabinfpdf/', ordendeventacabinfpdf, name="ordendeventacabinfpdf"),
    path('ordendeventacabinfexcel/', ordendeventacabinfexcel, name="ordendeventacabinfexcel"),
    path('ordendeventacabinfcsv/', ordendeventacabinfcsv, name="ordendeventacabinfcsv"),

    path('ordendeventadetinf_listar/', ordendeventadetinf_listar, name='ordendeventadetinf_listar'),
    path('ordendeventadetinfpdf/', ordendeventadetinfpdf, name="ordendeventadetinfpdf"),
    path('ordendeventadetinfexcel/', ordendeventadetinfexcel, name="ordendeventadetinfexcel"),
    path('ordendeventadetinfcsv/', ordendeventadetinfcsv, name="ordendeventadetinfcsv"),
    
]