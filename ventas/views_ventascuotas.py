from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils.datetime_safe import datetime

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import  desencriptar_datos2, encriptar_datos2
from ventas.models import Ventascuotas, Ventacab, Cliente


def ventascuotas_cargar(request,pk_token):
    if not request.user.has_perm('ventas.view_ventascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    if pk_token == "0":
        return redirect('ventascab_cargar', pk_token=0)

    pk_tokens = int(desencriptar_datos2(pk_token,request))
    objetos = Ventacab.objects.filter(idventacab=pk_tokens)
    for objeto in objetos:
        fecha= objeto.fecha
        nrofactura= objeto.nrofactura
        cliente= objeto.cliente
        total= f"{(objeto.total):,.0f}"

       # moneda= objeto.moneda,
       # cotizacion= objeto.cotizacion,


    contexto = {
        'habcmp': True,
        'habprov': True,
        'pkf': pk_token,
        'fecha': fecha,
        'nrofactura': nrofactura,
        'cliente': cliente,
        'total': total,
        'title': 'CUOTAS CLIENTES'
    }

    return render(request, "ventas/ventascuotas.html", contexto)

def ventascuotas_generar(request):
    if not request.user.has_perm('ventas.add_ventascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pkf = request.POST['pkf']
    idventacab = int(desencriptar_datos2(pkf,request))
    entrega =float(request.POST['entrega'])
    fechavto = request.POST['fechavto']
    cuota = float(request.POST['cuota'])
    monto = float(float(request.POST['monto']))
    entregainicial=0
    icuota=0
    imonto=0

    obj = Ventacab.objects.filter(idventacab=idventacab)
    idcliente = ([(detalle.idcliente_id) for detalle in obj])[0]

    if isinstance(entrega, int) or isinstance(entrega, float):
        entregainicial=entrega
    if isinstance(cuota, int) or isinstance(cuota, float):
        icuota = cuota
    if isinstance(monto, int) or isinstance(monto, float):
        imonto = monto

    ventacab_instance = Ventacab.objects.get(idventacab=idventacab)
    cliente_instance = Cliente.objects.get(pk=int(idcliente))  # Asegúrate de que `idcompracab` sea un entero

    ventascuotas = Ventascuotas.objects.filter(idventacab=idventacab)
    ventascuotas.delete()

    fechavto = datetime.strptime(fechavto, '%Y-%m-%d')
    contador = 0
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    while contador <= icuota:
        imontocuota=entregainicial
        if contador>0:
            fechavto = fechavto + timedelta(days=30)  # Sumamos 30 días (un mes aproximado)
            imontocuota=imonto

        if imontocuota>0:
            ventascuotas = Ventascuotas()
            ventascuotas.idventacab = ventacab_instance
            ventascuotas.orden = contador
            ventascuotas.idcliente=cliente_instance
            ventascuotas.fechavto = fechavto
            ventascuotas.monto = imontocuota
            ventascuotas.saldo = imontocuota
            ventascuotas.idempresa = didempresa
            ventascuotas.idsucursal = didsucursal
            ventascuotas.save()

        contador=contador+1

    response = {'success': True}
    return JsonResponse(response)

def ventascuotas_listar(request):
    if not request.user.has_perm('ventas.view_ventascuotas'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['id_pk']

    idventacab = int(desencriptar_datos2(pk,request))
    orden = request.POST['orden']
    formato = "%d-%m-%Y"  # Por ejemplo, "09-10-2023 15:30:00"
    print("idventacab  " + str(idventacab))

    if int(orden) == -1:
        objetos = Ventascuotas.objects.filter(idventacab=idventacab).order_by('orden')
        formato = "%d-%m-%Y"  # Por ejemplo, "09-10-2023 15:30:00"

    if int(orden) >=0:
        objetos = Ventascuotas.objects.filter(idventacab=idventacab,orden=orden)
        formato = "%y-%m-%d"  # Por ejemplo, "09-10-2023 15:30:00"

    datos = []
   # 'fechavto': objeto.fechavto.strftime(formato),

    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos2(objeto.idventascuotas,request),
            'orden': objeto.orden,
            'fechavto': objeto.fechavto.strftime(formato),
            'monto': f"{(objeto.monto):,.0f}",
            'monto2':objeto.monto,
        })

    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def ventascuotas_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_ventascuotas'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    pk = int(desencriptar_datos2(pk_token,request))

    objetos = Ventascuotas.objects.filter(idventascuotas=pk)
    for objeto in objetos:
        idventacab= objeto.idventacab

    ventascuotas = get_object_or_404(Ventascuotas, pk=pk)
    ventascuotas.delete()

    orden=0
    objetos = Ventascuotas.objects.filter(idventacab=idventacab,orden__gt=0).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    response = {'success': True, 'message': ''}
    return JsonResponse(response)


def ventascuotas_mod(request):
    if not request.user.has_perm('ventas.change_ventascuotas'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        idventacab = int(desencriptar_datos2(pkf,request))
        orden = request.POST['orden']
        monto = request.POST['monto']
        fechavto = request.POST['fechavto']

        objetos = Ventascuotas.objects.filter(idventacab=idventacab,orden=orden)
        for ventascuotas in objetos:
            idventascuotas=ventascuotas.idventascuotas

        ventacab_instance = Ventacab.objects.get(idventacab=idventacab)

        ventascuotas = get_object_or_404(Ventascuotas, pk=idventascuotas)
        ventascuotas.idventacab =ventacab_instance
        ventascuotas.orden = orden
        ventascuotas.fechavto = fechavto
        ventascuotas.monto = monto
        ventascuotas.saldo = monto
        ventascuotas.save()

        response = {'success': True}
        return JsonResponse(response)

def ventascuotas_guardar(request):
    if not request.user.has_perm('ventas.add_ventascuotas'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        idventacab = int(desencriptar_datos2(pkf,request))
        print("idventacab" +str(idventacab))
        monto = request.POST['monto']

        fechavto = request.POST['fechavto']

        obj = Ventacab.objects.filter(idventacab=idventacab)
        idcliente = ([(detalle.idcliente) for detalle in obj])[0]
        # print(" idcliente "+ str(idcliente)

        cantr = Ventascuotas.objects.filter(idventacab=idventacab ,orden__gt=0).count()+1
        print("cantr" +str(cantr))
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')

        ventascuotas = Ventascuotas()
        ventascuotas.idventacab =float(idventacab)
        ventascuotas.orden = cantr
        ventascuotas.fechavto = fechavto
        ventascuotas.monto = monto
        ventascuotas.idcliente = idcliente
        ventascuotas.saldo = monto
        ventascuotas.idempresa = idempresa
        ventascuotas.idsucursal = idsucursal

        ventascuotas.save()

        response = {'success': True}
        return JsonResponse(response)
