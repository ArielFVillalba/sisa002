
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *

from compras.views_presupdecompra_lst import *

urlpatterns = [
    path('presupdecompracab_inf/', presupdecompracab_inf, name='presupdecompracab_inf'),
    path('presupdecompracabinf_listar/', presupdecompracabinf_listar, name='presupdecompracabinf_listar'),
    path('presupdecompracabinfpdf/', presupdecompracabinfpdf, name="presupdecompracabinfpdf"),
    path('presupdecompracabinfexcel/', presupdecompracabinfexcel, name="presupdecompracabinfexcel"),
    path('presupdecompracabinfcsv/', presupdecompracabinfcsv, name="presupdecompracabinfcsv"),

    path('presupdecompradetinf_listar/', presupdecompradetinf_listar, name='presupdecompradetinf_listar'),
    path('presupdecompradetinfpdf/', presupdecompradetinfpdf, name="presupdecompradetinfpdf"),
    path('presupdecompradetinfexcel/', presupdecompradetinfexcel, name="presupdecompradetinfexcel"),
    path('presupdecompradetinfcsv/', presupdecompradetinfcsv, name="presupdecompradetinfcsv"),
    #path('compradetinfimp/', compradetinfimp, name="compradetinfimp"),

]