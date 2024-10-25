
from django.urls import path
from contabilidad.views_asiento import *

urlpatterns = [
    path('asiento/<str:cadena>/listar/',asiento_listar, name='asiento_listar'),
    path('asiento/<str:pk_token>/cargar/', asiento_cargar.as_view(), name='asiento_cargar'),
    path('asiento/crear/', asiento_crear.as_view(), name='asiento_crear'),
    path('asiento/<str:pk_token>/editar/', asiento_editar.as_view(), name='asiento_editar'),
    path('asiento/<str:pk_token>/eliminar/',asiento_eliminar.as_view(), name='asiento_eliminar'),
    path('asiento/<str:cadena>/listar/', asiento_listar, name='asiento_listar'),
    path('asiento_det_crear/', asiento_det_crear, name='asiento_det_crear'),
    path('asiento_det_actualizar/', asiento_det_actualizar, name='asiento_det_actualizar'),
    path('asiento_det/<str:pk_token>/eliminar/',asiento_det_eliminar.as_view(), name='asiento_det_eliminar'),
    path('bucardenominacion/', bucardenominacion, name='bucardenominacion'),
    path('buscarcuentalist/', buscarcuentalist, name='buscarcuentalist'),

]