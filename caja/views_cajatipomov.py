from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from caja.models import cajatipomov
from inicio.funcion import *


@permission_required('caja.view_cajatipomov')
def cajatipomovi(request):
    return render(request, "caja/cajatipomov.html")


def cajatipomov_editar(request):

    if not request.user.has_perm('caja.change_cajatipomov'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        tipomov = request.POST['tipomov'].upper()
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        var = True
        if tipomov is None or tipomov == "":
            var=False

        if var == False:
            response = {'success': False}
            return JsonResponse(response)

        diddep=""
        objetos = cajatipomov.objects.filter(tipomov=tipomov,idempresa=didempresa)
        for objeto in objetos:
            diddep = objeto.idcajatipomov

        if not diddep:
            deposito = cajatipomov()
            deposito.tipomov = tipomov
            deposito.idempresa = didempresa
            deposito.idsucursal = didsucursal
            deposito.save()

        response = {'success': True}
        return JsonResponse(response)


def cajatipomov_eliminar(request,pk_token):
    if not request.user.has_perm('caja.delete_cajatipomov'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    objetos = cajatipomov.objects.filter(tipomov=pk_token, idempresa=didempresa)
    objetos.delete()
    response = {'success': True}
    return JsonResponse(response)

def cajatipomov_listar(request):

    if not request.user.has_perm('caja.view_cajatipomov'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    objetos = cajatipomov.objects.filter(idempresa=didempresa)
    datos = []
    for objeto in objetos:
        print(str(objeto.tipomov))
        datos.append({
            'tipomov': objeto.tipomov,
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos

    Response = JsonResponse({'datos': datos})
    return Response


def cmbcajatipomov(request):
    if not request.user.has_perm('caja.view_cajatipomov'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        deposito = cajatipomov.objects.filter(idempresa=didempresa).values_list('tipomov', flat=True)
        nombres = list(deposito)
        Response = JsonResponse({'datos': nombres})
        return Response

