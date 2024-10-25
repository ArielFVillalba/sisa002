
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *
from caja.views_lstcajas import *

urlpatterns = [
    path('cajacierreinf/', cajacierreinf, name='cajacierreinf'),
    path('cajacierreinf_listar/', cajacierreinf_listar, name='cajacierreinf_listar'),
    path('cierrecajacabinfpdf/', cierrecajacabinfpdf, name="cierrecajacabinfpdf"),
    path('cierrecajacabinfexcel/', cierrecajacabinfexcel, name="cierrecajacabinfexcel"),
    path('cierrecajacabinfcsv/', cierrecajacabinfcsv, name="cierrecajacabinfcsv"),
    #path('compracabinfimp/', compracabinfimp, name="compracabinfimp"),

    #path('compradetinf_listar/', compradetinf_listar, name='compradetinf_listar'),
    #path('compradetinfpdf/', compradetinfpdf, name="compradetinfpdf"),
    #path('compradetinfexcel/', compradetinfexcel, name="compradetinfexcel"),

    #path('compradetinfcsv/', compradetinfcsv, name="compradetinfcsv"),
    #path('compradetinfimp/', compradetinfimp, name="compradetinfimp"),

]