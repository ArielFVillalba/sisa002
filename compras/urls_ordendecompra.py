
from django.contrib import admin
from django.urls import path
from compras.views_ordendecompra import *

urlpatterns = [
    path('ordencompcab_filtro/', ordencompcab_filtro, name='ordencompcab_filtro'),
    path('ordencompcab_filtro_lst/', ordencompcab_filtro_lst, name='ordencompcab_filtro_lst'),
    path('ordencompcab/<str:pk_token>/cargar/', ordencompcab_cargar.as_view(), name='ordencompcab_cargar'),
    path('ordencompcab/crear/', ordencompcab_crear.as_view(), name='ordencompcab_crear'),
    path('ordencompcab/<str:pk_token>/editar/', ordencompcab_editar.as_view(), name='ordencompcab_editar'),
    path('ordencompcab/<str:pk_token>/eliminar/', ordencompcab_eliminar.as_view(), name='ordencompcab_eliminar'),
    path('ordencompdet_listar/', ordencompdet_listar, name='ordencompdet_listar'),
    path('ordencompdet/<str:pk_token>/eliminar/', ordencompdet_eliminar, name='ordencompdet_eliminar'),
    path('ordencompdet_guardar/', ordencompdet_guardar, name='ordencompdetguardar'),
    path('ordencompdet_editar/', ordencompdet_editar, name='ordencompdetmod'),

]