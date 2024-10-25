from datetime import datetime

from contabilidad.models import asiento, asiento_det
from inicio.funcion import *
from django.shortcuts import get_object_or_404, redirect

def menucontabilidad(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')
        return render(request, 'contabilidad/menucontabilidad.html')
    else:
        return redirect('login')


def librodiario_listar2(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)

    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if cadena == "*"  or cadena == "0" or cadena == "":

        iasiento = asiento_det.objects.filter(idempresa=didempresa).order_by('idasiento.fecha','idasiento.nroasiento')
        listado_asientos = []

        # Recorrer los detalles y construir el nuevo objeto con los datos de asiento y asiento_det
        for detalle in listado_asientos:
            nuevo_objeto = {
                'pkas': encriptar_datos2(detalle.idasiento, request),
                'fecha': detalle.asiento.fecha,
                'nroasiento': detalle.idasiento.nroasiento,
                'cuenta': detalle.cuenta,
                'denominacio': detalle.denominacio,
                'descripcion': detalle.idasiento.descripcion,
                'debe': "{:,.0f}".format(float(detalle.debe)),
                'haber': "{:,.0f}".format(float(detalle.haber)),
                'pkasdet': encriptar_datos2(detalle.asiento.idasiento, request),
            }
            # Agregar el nuevo objeto a la lista
            listado_asientos.append(nuevo_objeto)

        for objeto in iasiento:
            objeto.pkasdet = encriptar_datos2(objeto.idasiento.idasiento, request)
            objeto.debe = "{:,.0f}".format(float(objeto.debe))
            objeto.haber = "{:,.0f}".format(float(objeto.haber))

        return render(request, 'contabilidad/libro_diario_listar.html', {'asiento': iasiento, 'cadena': '' })

    qs = asiento_det.objects.filter(idempresa=didempresa ,cuenta='')
    subcadenas = cadena.split(" ")
    for i in range(len(subcadenas)):

        qs1 = asiento.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs1)
        qs2 = asiento.objects.filter(descripcion__icontains=subcadenas[i], idempresa=didempresa)
        qs = qs.union(qs2)
        qs3 = asiento.objects.filter(nroasiento__icontains=subcadenas[i], idempresa=didempresa)
        qs = qs.union(qs3)

        icasiento = qs
        for objeto in icasiento:
            objeto.pkasdet = encriptar_datos2(objeto.idasiento.idasiento, request)
            objeto.debe = "{:,.0f}".format(float(objeto.debe))
            objeto.haber = "{:,.0f}".format(float(objeto.haber))

    return render(request, 'contabilidad/libro_diario_listar.html', {'asiento': icasiento ,'cadena': cadena})

def librodiario_listar(request, cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')

    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)

    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    # Filtrar los detalles de asiento por empresa
    iasiento = asiento_det.objects.filter(idempresa=didempresa).order_by('idasiento__fecha', 'idasiento__nroasiento','orden')
    print(str(iasiento))
    listado_asientos = []

    # Recorrer los detalles y construir el nuevo objeto con los datos de asiento y asiento_det
    for detalle in iasiento:
        nuevo_objeto = {
            'pkas': encriptar_datos2(detalle.idasiento.idasiento, request),  # encriptar id del asiento
            'fecha': detalle.idasiento.fecha,
            'nroasiento': detalle.idasiento.nroasiento,
            'cuenta': detalle.cuenta,
            'denominacion': detalle.denominacion,  # Asegúrate de que este campo existe en tu modelo
            'descripcion': detalle.idasiento.descripcion,
            'debe': "{:,.0f}".format(float(detalle.debe)),
            'haber': "{:,.0f}".format(float(detalle.haber)),
        }
        # Agregar el nuevo objeto a la lista
        listado_asientos.append(nuevo_objeto)

    # Enviar la lista a la plantilla
    return render(request, 'contabilidad/libro_diario_listar.html', {'asiento': listado_asientos, 'cadena': cadena})

def libro_diario_filtrar(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'contabilidad/libro_diario_filtrar.html')

def libro_diario_filtrar_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')

    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)

    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    fechaini = request.GET.get('fechaini', '')
    fechafin = request.GET.get('fechafin', '')

    vasiento = asiento_det.objects.filter(idempresa=didempresa).order_by('idasiento__fecha', 'idasiento__nroasiento','orden')

    if vasiento.exists() and fechaini:
        fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
        vasiento = vasiento.filter(idasiento__fecha__gte=fecha_inicio)
    if vasiento.exists() and fechafin:
        fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
        vasiento = vasiento.filter(idasiento__fecha__lte=fecha_fin)


    listado_asientos = []

    # Recorrer los detalles y construir el nuevo objeto con los datos de asiento y asiento_det
    for detalle in vasiento:
        nuevo_objeto = {
            'pkas': encriptar_datos2(detalle.idasiento.idasiento, request),  # encriptar id del asiento
            'fecha': detalle.idasiento.fecha,
            'nroasiento': detalle.idasiento.nroasiento,
            'cuenta': detalle.cuenta,
            'denominacion': detalle.denominacion,  # Asegúrate de que este campo existe en tu modelo
            'descripcion': detalle.idasiento.descripcion,
            'debe': "{:,.0f}".format(float(detalle.debe)),
            'haber': "{:,.0f}".format(float(detalle.haber)),
        }
        # Agregar el nuevo objeto a la lista
        listado_asientos.append(nuevo_objeto)

    return render(request, 'contabilidad/libro_diario_listar.html', {'asiento': listado_asientos, 'cadena': 0})
