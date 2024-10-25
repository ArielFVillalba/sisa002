
from django.urls import path
from caja.views_cajaconfiguracion import *

urlpatterns = [
    path('seriedet/<str:pk_token>/cargar/', seriedet_cargar.as_view(), name='seriedet_cargar'),
    path('seriedet/crear/', seriedet_crear.as_view(), name='seriedet_crear'),
    path('seriedet/<str:pk_token>/editar/', seriedet_editar.as_view(), name='seriedet_editar'),
    path('seriedet/<str:pk_token>/eliminar/', seriedet_eliminar.as_view(), name='seriedet_eliminar'),
    path('seriedet/listar/', seriedet_listar, name='seriedet_listar'),

]