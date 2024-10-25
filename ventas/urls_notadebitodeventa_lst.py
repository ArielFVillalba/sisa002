
from django.contrib import admin
from django.urls import path
from ventas import views
from ventas.views import *

from ventas.views_notadebitodeventa_lst import *

urlpatterns = [
    path('notadebitodeventacab_inf/', notadebitodeventacab_inf, name='notadebitodeventacab_inf'),
    path('notadebitodeventacabinf_listar/', notadebitodeventacabinf_listar, name='notadebitodeventacabinf_listar'),
    path('notadebitodeventacabinfpdf/', notadebitodeventacabinfpdf, name="notadebitodeventacabinfpdf"),
    path('notadebitodeventacabinfexcel/', notadebitodeventacabinfexcel, name="notadebitodeventacabinfexcel"),
    path('notadebitodeventacabinfcsv/', notadebitodeventacabinfcsv, name="notadebitodeventacabinfcsv"),

    path('notadebitodeventadetinf_listar/', notadebitodeventadetinf_listar, name='notadebitodeventadetinf_listar'),
    path('notadebitodeventadetinfpdf/', notadebitodeventadetinfpdf, name="notadebitodeventadetinfpdf"),
    path('notadebitodeventadetinfexcel/', notadebitodeventadetinfexcel, name="notadebitodeventadetinfexcel"),
    path('notadebitodeventadetinfcsv/', notadebitodeventadetinfcsv, name="notadebitodeventadetinfcsv"),
    
]