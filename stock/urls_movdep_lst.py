
from django.contrib import admin
from django.urls import path
from compras import views
from stock.views_movdep_lst import *


urlpatterns = [
    path('movdepcabinf/', movdepcabinf, name='movdepcabinf'),
    path('movdepcabinf_listar/', movdepcabinf_listar, name='movdepcabinf_listar'),
    path('movdepcabinfpdf/', movdepcabinfpdf, name="movdepcabinfpdf"),
    path('movdepcabinfexcel/', movdepcabinfexcel, name="movdepcabinfexcel"),
    path('movdepcabinfcsv/', movdepcabinfcsv, name="movdepcabinfcsv"),

    path('movdepdetinf_listar/', movdepdetinf_listar, name='movdepdetinf_listar'),
    path('movdepdetinfpdf/', movdepdetinfpdf, name="movdepdetinfpdf"),
    path('movdepdetinfexcel/', movdepdetinfexcel, name="movdepdetinfexcel"),
    path('movdepdetinfcsv/', movdepdetinfcsv, name="movdepdetinfcsv"),
    #path('compradetinfimp/', compradetinfimp, name="compradetinfimp"),

]