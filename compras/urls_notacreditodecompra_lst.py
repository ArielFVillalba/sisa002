
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *

from compras.views_notacreditodecompra_lst import *

urlpatterns = [

    path('notacreddecompracab_inf/', notacreddecompracab_inf, name='notacreddecompracab_inf'),
    path('notacreddecompracabinf_listar/', notacreddecompracabinf_listar, name='notacreddecompracabinf_listar'),
    path('notacreddecompracabinfpdf/', notacreddecompracabinfpdf, name="notacreddecompracabinfpdf"),
    path('notacreddecompracabinfexcel/', notacreddecompracabinfexcel, name="notacreddecompracabinfexcel"),
    path('notacreddecompracabinfcsv/', notacreddecompracabinfcsv, name="notacreddecompracabinfcsv"),

    path('notacreddecompradetinf_listar/', notacreddecompradetinf_listar, name='notacreddecompradetinf_listar'),
    path('notacreddecompradetinfpdf/', notacreddecompradetinfpdf, name="notacreddecompradetinfpdf"),
    path('notacreddecompradetinfexcel/', notacreddecompradetinfexcel, name="notacreddecompradetinfexcel"),
    path('notacreddecompradetinfcsv/', notacreddecompradetinfcsv, name="notacreddecompradetinfcsv"),
    #path('compradetinfimp/', compradetinfimp, name="compradetinfimp"),

]