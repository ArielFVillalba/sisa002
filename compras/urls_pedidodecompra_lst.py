
from django.contrib import admin
from django.urls import path
from compras import views
from compras.views import *

from compras.views_pedidodecompra_lst import *

urlpatterns = [
    path('pedidodecompracab_inf/', pedidodecompracab_inf, name='pedidodecompracab_inf'),
    path('pedidodecompracabinf_listar/', pedidodecompracabinf_listar, name='pedidodecompracabinf_listar'),
    path('pedidodecompracabinfpdf/', pedidodecompracabinfpdf, name="pedidodecompracabinfpdf"),
    path('pedidodecompracabinfexcel/', pedidodecompracabinfexcel, name="pedidodecompracabinfexcel"),
    path('pedidpdecompracabinfcsv/', pedidpdecompracabinfcsv, name="pedidpdecompracabinfcsv"),

    path('pedidodecompradetinf_listar/', pedidodecompradetinf_listar, name='pedidodecompradetinf_listar'),
    path('pedidodecompradetinfpdf/', pedidodecompradetinfpdf, name="pedidodecompradetinfpdf"),
    path('pedidodecompradetinfexcel/', pedidodecompradetinfexcel, name="pedidodecompradetinfexcel"),
    path('pedidodecompradetinfcsv/', pedidodecompradetinfcsv, name="pedidodecompradetinfcsv"),

]