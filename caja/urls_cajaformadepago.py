
from django.contrib import admin
from django.urls import path

from caja.views_cajaformadepago import *

urlpatterns = [
    path('cajaformadepagov/',cajaformadepagov, name='cajaformadepagov'),
    path('cajaformadepago_listar/', cajaformadepago_listar, name='cajaformadepago_listar'),
    path('cajaformadepago_editar/', cajaformadepago_editar, name='cajaformadepago_editar'),
    path('cajaformadepago/<str:pk_token>/eliminar/', cajaformadepago_eliminar, name='cajaformadepago_eliminar'),
    path('cmbcajaformadepago/', cmbcajaformadepago, name="cmbcajaformadepago"),
]