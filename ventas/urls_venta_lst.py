
from django.contrib import admin
from django.urls import path
from ventas import views
from ventas.views import *

from ventas.views_venta_lst import *

urlpatterns = [
    path('ventacabinf/', ventacabinf, name='ventacabinf'),
    path('ventacabinf_listar/', ventacabinf_listar, name='ventacabinf_listar'),
    path('ventacabinfpdf/', ventacabinfpdf, name="ventacabinfpdf"),
    path('ventacabinfexcel/', ventacabinfexcel, name="ventacabinfexcel"),
    path('ventacabinfcsv/', ventacabinfcsv, name="ventacabinfcsv"),
    #path('ventacabinfimp/', ventacabinfimp, name="ventacabinfimp"),

    path('ventadetinf_listar/', ventadetinf_listar, name='ventadetinf_listar'),
    path('ventadetinfpdf/', ventadetinfpdf, name="ventadetinfpdf"),
    path('ventadetinfexcel/', ventadetinfexcel, name="ventadetinfexcel"),
    path('ventadetinfcsv/', ventadetinfcsv, name="ventadetinfcsv"),
    #path('ventadetinfimp/', ventadetinfimp, name="ventadetinfimp"),

]