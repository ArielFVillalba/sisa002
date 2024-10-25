from django.urls import path, include
from caja.views import *

urlpatterns = [
    path('', include('caja.urls_ventacaja')),
    path('', include('caja.urls_cajatipomov')),
    path('', include('caja.urls_cajaapecierre')),
    path('', include('caja.urls_cajaformadepago')),
    path('', include('caja.urls_cajalstcierrecaja')),
    path('', include('caja.urls_cajaconfiguracion')),
    path('menucaja/', menucaja, name="menucaja"),
    path('movcaja/', movcaja, name="movcaja"),

]
