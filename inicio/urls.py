
from django.contrib import admin
from django.urls import path
from inicio import views
from django.conf.urls import handler404

urlpatterns = [
   # path('login/', views.login, name="login"),
    path('current_time/',views.current_time, name='current_time'),
    path('logoini/', views.logoini, name="logoini"),
    path('menuini/', views.menuini, name="menuini"),
    path('menu/', views.menu, name="menu"),
    path('buscar_usuario/', views.buscar_usuario, name="buscar_usuario"),
    path('base/', views.base, name="base"),
    path('base2/', views.base2, name="base2"),
    path('sisa/', views.sisa, name="sisa"),
    path('login2/', views.login2, name="login2"),
    path('login/', views.loginc, name='login'),
    path('pagcofirmacion/', views.pagcofirmacion, name='pagcofirmacion'),
    path('empsucursal/', views.empsucursal, name="empsucursal"),
    path('sucursales/', views.sucursales, name="sucursales"),
]
