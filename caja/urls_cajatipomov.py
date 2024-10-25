
from django.urls import path

from caja.views_cajatipomov import *

urlpatterns = [
    path('cajatipomovi/',cajatipomovi, name='cajatipomovi'),
    path('cajatipomov_listar/', cajatipomov_listar, name='cajatipomov_listar'),
    path('cajatipomov_editar/', cajatipomov_editar, name='cajatipomov_editar'),
    path('cajatipomov/<str:pk_token>/eliminar/', cajatipomov_eliminar, name='cajatipomov_eliminar'),
    path('cmbcajatipomov/', cmbcajatipomov, name="cmbcajatipomov"),

]