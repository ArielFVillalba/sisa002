
from django.contrib import admin
from django.urls import path, include
from stock import views
from stock.views import *
from stock.views_articulos import *
from stock.views_familia import *

urlpatterns = [
    path('', include('stock.urls_movdep')),
    path('', include('stock.urls_movdep_lst')),
    path('', include('stock.urls_stock_lst')),
    path('', include('stock.urls_inventario')),

    path('menustock/', views.menustock, name="menustock"),

    path('articulos/<str:cadena>/listar/', articulos_listar, name='articulos_listar'),
    path('articulos/crear/', articulos_crear.as_view(), name='articulos_crear'),
    path('articulos/<str:pk_token>/cargar/', articulos_cargar.as_view(), name='articulos_cargar'),
    path('articulos/<str:pk_token>/editar/', articulos_editar.as_view(), name='articulos_editar'),
    path('articulos/<str:pk_token>/eliminar/', articulos_eliminar.as_view(), name='articulos_eliminar'),
    path('articulosubirimagen/', articulosubirimagen, name='articulosubirimagen'),

    path('familia/<str:cadena>/listar/', familia_listar, name='familia_listar'),
    path('familia/crear/', familia_crear.as_view(), name='familia_crear'),
    path('familia/<str:pk_token>/cargar/', familia_cargar.as_view(), name='familia_cargar'),
    path('familia/<str:pk_token>/editar/', familia_editar.as_view(), name='familia_editar'),
    path('familia/<str:pk_token>/eliminar/', familia_eliminar.as_view(), name='familia_eliminar'),
    path('cmbfamilia/', cmbfamilia, name='cmbfamilia'),
    path('familia_buscar/', familia_buscar, name='familia_buscar'),

    path('articulodatos/', articulodatos, name='articulodatos'),
    path('articulodatosdesc/', articulodatosdesc, name='articulodatosdesc'),
    path('cmbarticulo/', cmbarticulo, name='cmbarticulo'),
    path('deposito/', deposito, name='deposito'),
    path('deposito_listar/', deposito_listar, name='deposito_listar'),
    path('deposito_editar/', deposito_editar, name='deposito_editar'),
    path('deposito/<str:pk_token>/eliminar/', deposito_eliminar, name='deposito_eliminar'),
    path('cmbdep/', cmbdep, name="cmbdep"),
    path('sucursalesdep/', sucursalesdep, name="sucursalesdep"),

]
