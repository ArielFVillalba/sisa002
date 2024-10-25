
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *
from compras.views_compra_lst import *

urlpatterns = [
    path('compracabinf/', compracabinf, name='compracabinf'),
    path('compracabinf_listar/', compracabinf_listar, name='compracabinf_listar'),
    path('compracabinfpdf/', compracabinfpdf, name="compracabinfpdf"),
    path('compracabinfexcel/', compracabinfexcel, name="compracabinfexcel"),
    path('compracabinfcsv/', compracabinfcsv, name="compracabinfcsv"),
    #path('compracabinfimp/', compracabinfimp, name="compracabinfimp"),

    path('compradetinf_listar/', compradetinf_listar, name='compradetinf_listar'),
    path('compradetinfpdf/', compradetinfpdf, name="compradetinfpdf"),
    path('compradetinfexcel/', compradetinfexcel, name="compradetinfexcel"),
    path('compradetinfcsv/', compradetinfcsv, name="compradetinfcsv"),
    #path('compradetinfimp/', compradetinfimp, name="compradetinfimp"),

]