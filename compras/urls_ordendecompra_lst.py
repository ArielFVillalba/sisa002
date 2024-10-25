
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *

from compras.views_ordendecompra_lst import *

urlpatterns = [
    path('ordendecompracab_inf/', ordendecompracab_inf, name='ordendecompracab_inf'),
    path('ordendecompracabinf_listar/', ordendecompracabinf_listar, name='ordendecompracabinf_listar'),
    path('ordendecompracabinfpdf/', ordendecompracabinfpdf, name="ordendecompracabinfpdf"),
    path('ordendecompracabinfexcel/', ordendecompracabinfexcel, name="ordendecompracabinfexcel"),
    path('ordendecompracabinfcsv/', ordendecompracabinfcsv, name="ordendecompracabinfcsv"),

    path('ordendecompradetinf_listar/', ordendecompradetinf_listar, name='ordendecompradetinf_listar'),
    path('ordendecompradetinfpdf/', ordendecompradetinfpdf, name="ordendecompradetinfpdf"),
    path('ordendecompradetinfexcel/', ordendecompradetinfexcel, name="ordendecompradetinfexcel"),
    path('ordendecompradetinfcsv/', ordendecompradetinfcsv, name="ordendecompradetinfcsv"),
    #path('compradetinfimp/', compradetinfimp, name="compradetinfimp"),

]