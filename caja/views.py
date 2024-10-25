from django.shortcuts import render
from inicio.funcion import *

def menucaja(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, 'caja/menucaja.html')
    else:
        return redirect('login')


def tipomovcaja(request):
    if request.user.is_authenticated:

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, 'caja/tipomov.html')
    else:
        return redirect('login')

def movcaja(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, 'caja/menucaja.html')
    else:
        return redirect('login')

