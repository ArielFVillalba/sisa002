from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.template import context

from .forms import *
from django.apps import AppConfig
from django.apps import AppConfig

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

con1=1

# Create your views here.
from inicio.funcion import *

def infrendprov(request):
    if request.user.is_authenticated:
        return render(request, "informeprov/infrendprov.html")
    else:
        return redirect('login')


def menucompras(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        return render(request, 'compras/menucompras.html')
    else:
        return redirect('login')

def menuproveedor(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, 'compras/menuproveedor.html')
    else:
        return redirect('login')

