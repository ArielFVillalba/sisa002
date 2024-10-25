from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils.datetime_safe import datetime

from compras.models import Compracab, Comprascuotas
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import  desencriptar_datos2, encriptar_datos2


def comprascuotas_cargar(request,pk_token):
    if not request.user.has_perm('compras.view_comprascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response


    if pk_token == "0":
        return redirect('compracab_cargar', pk_token=0)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    pk_tokens = int(desencriptar_datos2(pk_token,request))
    objetos = Compracab.objects.filter(idcompracab=pk_tokens)
    for objeto in objetos:
        fecha= objeto.fecha
        nrofactura= objeto.nrofactura
        proveedor= objeto.proveedor
        total= f"{(objeto.total):,.0f}"


       # moneda= objeto.moneda,
       # cotizacion= objeto.cotizacion,


    print(nrofactura)
    contexto = {
        'habcmp': True,
        'habprov': True,
        'pkf': pk_token,
        'fecha': fecha,
        'nrofactura': nrofactura,
        'proveedor': proveedor,
        'total': total,
        'title': 'CUOTAS PROVEEDOR'
    }

    return render(request, "compras/comprascuotas.html", contexto)

def comprascuotas_generar(request):
    if not request.user.has_perm('compras.add_comprascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pkf = request.POST['pkf']
    idcompracab = int(desencriptar_datos2(pkf,request))
    entrega =float(request.POST['entrega'])
    fechavto = request.POST['fechavto']
    cuota = float(request.POST['cuota'])
    monto = float(float(request.POST['monto']))
    entregainicial=0
    icuota=0
    imonto=0


    obj = Compracab.objects.filter(idcompracab=idcompracab)
    idproveedor = ([(detalle.idproveedor) for detalle in obj])[0]

    if isinstance(entrega, int) or isinstance(entrega, float):
        entregainicial=entrega
    if isinstance(cuota, int) or isinstance(cuota, float):
        icuota = cuota
    if isinstance(monto, int) or isinstance(monto, float):
        imonto = monto

    comprascuotas = Comprascuotas.objects.filter(idcompracab=idcompracab)
    comprascuotas.delete()

    fechavto = datetime.strptime(fechavto, '%Y-%m-%d')
    contador = 0

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    compracab_instance = Compracab.objects.get(pk=int(idcompracab))  # Asegúrate de que `idcompracab` sea un entero

    while contador <= icuota:
        imontocuota=entregainicial
        if contador>0:
            fechavto = fechavto + timedelta(days=30)  # Sumamos 30 días (un mes aproximado)
            imontocuota=imonto

        if imontocuota>0:
            comprascuotas = Comprascuotas()
            comprascuotas.idcompracab = compracab_instance
            comprascuotas.orden = contador
            comprascuotas.fechavto = fechavto
            comprascuotas.monto = imontocuota
            comprascuotas.saldo = imontocuota
            comprascuotas.idempresa = didempresa
            comprascuotas.idsucursal = didsucursal
            comprascuotas.idproveedor=idproveedor
            comprascuotas.save()
        contador=contador+1

    response = {'success': True}
    return JsonResponse(response)


def comprascuotas_listar(request):
    if not request.user.has_perm('compras.view_comprascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['id_pk']
    #print("comprascuotas_listar  "+ str(pk))
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    idcompracab = int(desencriptar_datos2(pk,request))
    orden = request.POST['orden']
    formato = "%d-%m-%Y"  # Por ejemplo, "09-10-2023 15:30:00"

    if int(orden) == -1:
        objetos = Comprascuotas.objects.filter(idcompracab=idcompracab).order_by('orden')
        formato = "%d-%m-%Y"  # Por ejemplo, "09-10-2023 15:30:00"

    if int(orden) >=0:
        objetos = Comprascuotas.objects.filter(idcompracab=idcompracab,orden=orden)
        formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"


    datos = []
   # 'fechavto': objeto.fechavto.strftime(formato),

    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos2(objeto.idcomprascuotas,request),
            'orden': objeto.orden,
            'fechavto': objeto.fechavto.strftime(formato),
            'monto': f"{(objeto.monto):,.0f}",
            'monto2':objeto.monto,

        })

    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def comprascuotas_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_comprascuotas'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    pk = int(desencriptar_datos2(pk_token,request))

    objetos = Comprascuotas.objects.filter(idcomprascuotas=pk)
    for objeto in objetos:
        idcompracab= objeto.idcompracab

    comprascuotas = get_object_or_404(Comprascuotas, pk=pk)
    comprascuotas.delete()

    orden=0
    objetos = Comprascuotas.objects.filter(idcompracab=idcompracab,orden__gt=0).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    response = {'success': True, 'message': ''}
    return JsonResponse(response)


def comprascuotas_mod(request):
    if not request.user.has_perm('compras.change_comprascuotas'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        idcompracab = int(desencriptar_datos2(pkf,request))
        compracab_instance = Compracab.objects.get(pk=int(idcompracab))  # Asegúrate de que `idcompracab` sea un entero

        orden = request.POST['orden']
        monto = request.POST['monto']
        fechavto = request.POST['fechavto']

        objetos = Comprascuotas.objects.filter(idcompracab=idcompracab,orden=orden)
        for comprascuotas in objetos:
            idcomprascuotas=comprascuotas.idcomprascuotas

        comprascuotas = get_object_or_404(Comprascuotas, pk=idcomprascuotas)
        comprascuotas.idcompracab =compracab_instance
        comprascuotas.orden = orden
        comprascuotas.fechavto = fechavto
        comprascuotas.monto = monto
        comprascuotas.save()

        response = {'success': True}
        return JsonResponse(response)

def comprascuotas_guardar(request):
    if not request.user.has_perm('compras.add_comprascuotas'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        idcompracab = int(desencriptar_datos2(pkf,request))
        #print("idcompracab" +str(idcompracab))
        monto = request.POST['monto']
        #print("monto" +str(monto))

        fechavto = request.POST['fechavto']
        #print("fechavto" +str(fechavto))

        cantr = Comprascuotas.objects.filter(idcompracab=idcompracab ,orden__gt=0).count()+1

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        compracab_instance = Compracab.objects.get(pk=int(idcompracab))  # Asegúrate de que `idcompracab` sea un entero

        comprascuotas = Comprascuotas()
        comprascuotas.idcompracab =compracab_instance
        comprascuotas.orden = cantr
        comprascuotas.fechavto = fechavto
        comprascuotas.monto = monto
        comprascuotas.idempresa = didempresa
        comprascuotas.idsucursal = didsucursal
        comprascuotas.save()

        response = {'success': True}
        return JsonResponse(response)
