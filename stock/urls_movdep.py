
from django.contrib import admin
from django.urls import path
from stock.views_movdep import *

urlpatterns = [
    path('movdepcab_filtro/', movdepcab_filtro, name='movdepcab_filtro'),
    path('movdepcab_filtro_lst/', movdepcab_filtro_lst, name='movdepcab_filtro_lst'),

    path('movdepcab_filtro/', movdepcab_filtro, name='movdepcab_filtro'),
    path('movdepcab_filtro_lst/', movdepcab_filtro_lst, name='movdepcab_filtro_lst'),
    path('movdepcab/<str:pk_token>/cargar/', movdepcab_cargar.as_view(), name='movdepcab_cargar'),
    path('movdepcab/<str:cadena>/listar/', movdepcab_listar, name='movdepcab_listar'),
    path('movdepcab/crear/', movdepcab_crear.as_view(), name='movdepcab_crear'),
    path('movdepcab/<str:pk_token>/editar/', movdepcab_editar.as_view(), name='movdepcab_editar'),
    path('movdepcab/<str:pk_token>/eliminar/', movdepcab_eliminar.as_view(), name='movdepcab_eliminar'),
    path('movdepdet_listar/', movdepdet_listar, name='movdepdet_listar'),
    path('movdepdet_guardar/', movdepdet_guardar, name='movdepdet_guardar'),
    path('movdepdet_editar/', movdepdet_editar, name='movdepdet_editar'),
    path('movdepdet/<str:pk_token>/eliminar/', movdepdet_eliminar, name='movdepdet_eliminar'),


]
