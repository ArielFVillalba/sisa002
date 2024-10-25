from django.shortcuts import render, redirect

from inicio.funcion import  desencriptar_datos2


# Create your views here.

def menuventas(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, "ventas/menuventas.html")
    else:
        return redirect('login')

def menucliente(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')
        request.session['caja'] = 0
        request.session['pkfa']=""
        return render(request, 'ventas/menucliente.html')
    else:
        return redirect('login')
