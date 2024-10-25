from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import JsonResponse
from caja.models import cajaformadepago
from inicio.funcion import *

@permission_required('caja.view_cajaformadepago')
def cajaformadepagov(request):
    return render(request, "caja/cajaformadepago.html")

def cajaformadepago_editar(request):
    if not request.user.has_perm('caja.add_cajaformadepago'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        formadepago = request.POST['formadepago'].upper()
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        var = True
        if formadepago is None or formadepago == "":
            var=False


        if var == False:
            response = {'success': False}
            return JsonResponse(response)
        print(str(formadepago))
        diddep=""
        objetos = cajaformadepago.objects.filter(idempresa=didempresa,formadepago=formadepago)

        for objeto in objetos:
            diddep = objeto.idformadepago

        if not diddep:
            aformadepago = cajaformadepago()
            aformadepago.formadepago = str(formadepago)
            aformadepago.idempresa = didempresa
            aformadepago.idsucursal = didsucursal
            aformadepago.save()

        response = {'success': True}
        return JsonResponse(response)


def cajaformadepago_eliminar(request,pk_token):
    if not request.user.has_perm('caja.delete_cajaformadepago'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    objetos = cajaformadepago.objects.filter(formadepago=pk_token, idempresa=didempresa)
    objetos.delete()
    response = {'success': True}
    return JsonResponse(response)

def cajaformadepago_listar(request):
    if not request.user.has_perm('caja.view_cajaformadepago'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')



    objetos =cajaformadepago.objects.filter(idempresa=didempresa)
    datos = []
    for objeto in objetos:
        print(str(objeto.formadepago))
        datos.append({
            'formadepago': objeto.formadepago,
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos

    Response = JsonResponse({'datos': datos})
    return Response


def cmbcajaformadepago(request):
    if not request.user.has_perm('caja.view_cajaformadepago'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)
    if request.method == 'POST':
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        formadepago = cajaformadepago.objects.filter(idempresa=didempresa).values_list('formadepago', flat=True)
        nombres = list(formadepago)
        Response = JsonResponse({'datos': nombres})
        return Response

