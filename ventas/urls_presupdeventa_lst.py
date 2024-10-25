
from django.contrib import admin
from django.urls import path
from ventas import views
from ventas.views import *

from ventas.views_presupdeventa_lst import *

urlpatterns = [
    path('presupdeventacab_inf/', presupdeventacab_inf, name='presupdeventacab_inf'),
    path('presupdeventacabinf_listar/', presupdeventacabinf_listar, name='presupdeventacabinf_listar'),
    path('presupdeventacabinfpdf/', presupdeventacabinfpdf, name="presupdeventacabinfpdf"),
    path('presupdeventacabinfexcel/', presupdeventacabinfexcel, name="presupdeventacabinfexcel"),
    path('presupdeventacabinfcsv/', presupdeventacabinfcsv, name="presupdeventacabinfcsv"),

    path('presupdeventadetinf_listar/', presupdeventadetinf_listar, name='presupdeventadetinf_listar'),
    path('presupdeventadetinfpdf/', presupdeventadetinfpdf, name="presupdeventadetinfpdf"),
    path('presupdeventadetinfexcel/', presupdeventadetinfexcel, name="presupdeventadetinfexcel"),
    path('presupdeventadetinfcsv/', presupdeventadetinfcsv, name="presupdeventadetinfcsv"),
    
]