
from django.urls import path
from caja.views_ventacaja import *

urlpatterns = [
    path('ventacaja_filtro/',ventacaja_filtro, name='ventacaja_filtro'),
    path('ventacaja_filtro_lst/', ventacaja_filtro_lst, name='ventacaja_filtro_lst'),
    path('ventacaja/<str:cadena>/listar/', ventacaja_listar, name='ventacaja_listar'),
    path('ventadet_caja_listar/', ventadet_caja_listar, name='ventadet_caja_listar'),

    path('ventacaja/<str:pk_token>/cargar/', ventacaja_cargar.as_view(), name='ventacaja_cargar'),
    path('ventadetcaja_guardar/', ventadetcaja_guardar, name='ventadetcaja_guardar'),
    path('ventadetcaja/<str:pk_token>/eliminar/', ventadetcaja_eliminar, name='ventadetcaja_eliminar'),

    path('ventacierre/<str:pk_token>/cargar/', ventacierre_cargar.as_view(), name='ventacierre_cargar'),
    path('detallepagocaja_listar/', detallepagocaja_listar, name='detallepagocaja_listar'),
    path('ventacajapago_guardar/', ventacajapago_guardar, name='ventacajapago_guardar'),
    path('cajapagocli/<str:pk_token>/eliminar/',cajapagocli_eliminar.as_view(), name='cajapagocli_eliminar'),
    path('ventacaja/<str:pk_token>/cerrarventa/', ventacaja_cerrarventa, name='ventacaja_cerrarventa'),
    path('imprimirticket/', imprimirticket, name='imprimirticket'),
    path('check_tickets/', check_tickets, name='check_tickets'),

]