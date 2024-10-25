
from django.urls import path
from compras.views_compra import *

urlpatterns = [

    path('compracab_filtro/',compracab_filtro, name='compracab_filtro'),
    path('compracab_filtro_lst/', compracab_filtro_lst, name='compracab_filtro_lst'),
    path('compracab/<str:cadena>/listar/', compracab_listar, name='compracab_listar'),
    path('compracab/<str:pk_token>/cargar/', compracab_cargar.as_view(), name='compracab_cargar'),
    path('compracab/crear/', compracab_crear.as_view(), name='compracab_crear'),
    path('compracab/<str:pk_token>/editar/', compracab_editar.as_view(), name='compracab_editar'),
    path('compracab/<str:pk_token>/editar/', compracab_editar2.as_view(), name='compracab_editar'),
    path('compracab/<str:pk_token>/eliminar/', CompraCabEliminar.as_view(), name='compracab_eliminar'),
    path('compradet_listar/', compradet_listar, name='compradet_listar'),
    path('compradet/<str:pk_token>/eliminar/', compradet_eliminar, name='compradet_eliminar'),
    path('guardardet/', guardardet, name='guardardet'),
    path('compradetmod/', compradetmod, name='compradetmod'),

]