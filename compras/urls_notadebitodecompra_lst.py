
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *

from compras.views_notadebitodecompra_lst import *

urlpatterns = [

    path('notadebdecompracab_inf/', notadebdecompracab_inf, name='notadebdecompracab_inf'),
    path('notadebdecompracabinf_listar/', notadebdecompracabinf_listar, name='notadebdecompracabinf_listar'),
    path('notadebdecompracabinfpdf/', notadebdecompracabinfpdf, name="notadebdecompracabinfpdf"),
    path('notadebdecompracabinfexcel/', notadebdecompracabinfexcel, name="notadebdecompracabinfexcel"),
    path('notadebdecompracabinfcsv/', notadebdecompracabinfcsv, name="notadebdecompracabinfcsv"),

    path('notadebdecompradetinf_listar/', notadebdecompradetinf_listar, name='notadebdecompradetinf_listar'),
    path('notadebdecompradetinfpdf/', notadebdecompradetinfpdf, name="notadebdecompradetinfpdf"),
    path('notadebdecompradetinfexcel/', notadebdecompradetinfexcel, name="notadebdecompradetinfexcel"),
    path('notadebdecompradetinfcsv/', notadebdecompradetinfcsv, name="notadebdecompradetinfcsv"),
    #path('compradetinfimp/', compradetinfimp, name="compradetinfimp"),

]