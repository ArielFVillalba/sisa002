from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from caja.forms import CajaapertcierreForm
from caja.models import cajaapertcierre, cajaapertcierredet, seriedet, cajaventapago
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from ventas.models import Ventacab

from django.db.models import Sum
from django.shortcuts import render, redirect

def cajaapertura(request):

    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'caja/apertura.html')


def cajaaperturacierre(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'caja/cajaapcierre.html')

class cajaapertura_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'caja.view_cajaapertcierre'
    model = cajaapertcierre
    form_class = CajaapertcierreForm
    template_name = 'caja/apertura.html'
    success_url = reverse_lazy('cajaapertura_cargar')

    def get(self, request):
        skey = iskey(request)
        cajaapertc = None
        totalfactura=0
        facturafin=0

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        print('pasa aqui cajaapertura_cargar ')
        cajaapertc = cajaapertcierre.objects.filter(idempresa=didempresa,facturafin='')
        cantr = cajaapertc.count()
        if cantr > 0:
            return redirect('menucaja')

        context = {'cjap': cajaapertc}  # Crear un diccionario de contexto
        context['title'] = ' APETURA '
        context['sidr'] = '/cajaapertura_guardar/'

        return render(request, self.template_name, context)

@permission_required('caja.add_cajaapertcierre')
def cajaapertura_guardar(request):

    if request.method == 'POST':
        skey = iskey(request)
        cajaapertc = None
        totalfactura=0
        facturafin=0
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        apertura = request.POST.get('apertura')
        id_usuario = request.user.id

        cajaapertc = cajaapertcierre.objects.filter(iddocumentos=1,idusuario=id_usuario, idempresa=didempresa,facturafin='')
        cantr = cajaapertc.count()
        print(' cajaapertc '+str(cantr))
        if cantr > 0:
            return redirect('menucaja')

        objetos = seriedet.objects.filter(iddocumentos=1,idusuario=id_usuario,idempresa=didempresa)
        cantr = objetos.count()
        print(' seriedet '+str(cantr))
        if cantr == 0:
            return redirect('menucaja')

        correlativa = ([detalle.correlativa for detalle in objetos])[0] if objetos else '0'
        timbrado = ([detalle.timbrado for detalle in objetos])[0] if objetos else '0'
        iddocumentos = ([detalle.iddocumentos for detalle in objetos])[0] if objetos else '0'
        deposito= ([detalle.deposito for detalle in objetos])[0] if objetos else '0'
        nrocaja= ([detalle.nrocaja for detalle in objetos])[0] if objetos else '0'

        print(' correlativa  ' +str(correlativa) +' timbrado  ' +str(timbrado) +' iddocumentos  ' +str(iddocumentos) +' deposito  ' +str(deposito) +' nrocaja  ' +str(nrocaja)   )

        if correlativa == 0 or timbrado == 0 or iddocumentos == 0 or deposito == 0 or nrocaja == 0:
            return redirect('menucaja')

        # Obtener la fecha actual
        fecha_actual = datetime.now()
        # Formatear la fecha como año-mes-día
        fecha = fecha_actual.strftime("%Y-%m-%d")
        id_usuario = request.user.id

        cajaapc = cajaapertcierre()
        cajaapc.fecha = fecha
        cajaapc.apertura = apertura
        cajaapc.facturaini = correlativa
        cajaapc.timbrado = timbrado
        cajaapc.iddocumentos = iddocumentos
        cajaapc.nrocaja = nrocaja
        cajaapc.idempresa = didempresa
        cajaapc.idsucursal = didsucursal
        cajaapc.idusuario = id_usuario
        cajaapc.save()

        return redirect('ventacaja_cargar', pk_token=0)


class cajaapcierre_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'caja.view_cajaapertcierre'
    model = cajaapertcierre
    form_class = CajaapertcierreForm
    template_name = 'caja/cajaapcierre.html'
    success_url = reverse_lazy('cajaapcierre_cargar')

    def get(self, request,pk_token):
        skey = iskey(request)
        cajaapertc = None
        totalfactura=0
        facturafin=0
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')


        #pk_token=1
        #pk_token = encriptar_datos(pk_token, skey)
        id_usuario = request.user.id

        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            cajaapertc = cajaapertcierre.objects.filter(idcajaapertcierre=pk_desencriptado)  # Recuperar la compra por su clave primaria
        else:
            cajaapertc = cajaapertcierre.objects.filter(idusuario =id_usuario,idempresa=didempresa, facturafin='')

            #cajaapertc2 = cajaapertcierre.objects.filter(idempresa=didempresa, idsucursal=didsucursal)

            #cajaapertc=cajaapertc1.union(cajaapertc2)
            cantr = cajaapertc.count()
            print(' cant reg cajaapertc '+str(cantr))
            if cantr == 0:
                return redirect('menucaja')

            pk_token = ([detalle.idcajaapertcierre for detalle in cajaapertc])[0] if cajaapertc else '0'
            facturaini = ([detalle.facturaini for detalle in cajaapertc])[0] if cajaapertc else '0'
            pk_token = encriptar_datos2(pk_token,request)
            nrocaja = ([detalle.nrocaja for detalle in cajaapertc])[0] if cajaapertc else '0'


        qs = Ventacab.objects.filter(nrocaja=nrocaja,idempresa=didempresa,nrofactura__gte=facturaini)
        totalfactura = sum([detalle.total for detalle in qs])
        totalfactura=f"{totalfactura:,.0f}"
        obj = seriedet.objects.filter(idserie=1,iddocumentos=1,idempresa=didempresa,idsucursal=didsucursal)
        facturafin = ([detalle.correlativa for detalle in obj])[0] if obj else '0'

        facturafin=int(facturafin)-1

        if int(facturaini)>int(facturafin):
            facturafin=0
        cajaapertc = cajaapertc.get()
        context = {'cjap': cajaapertc}  # Crear un diccionario de contexto
        context['title'] = 'CIERRE - CAJA '
        context['sidr'] = '/cajaapcierre/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['pk_token'] = pk_token
        context['totalfactura'] = totalfactura
        context['facturafin'] = facturafin
        context['hab1']= True
        context['hab2']= False
        return render(request, self.template_name, context)

def cajaapcierre_cerrar(request,pk_token):
    if not request.user.has_perm('caja.change_cajaapertcierre'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    skey = iskey(request)
    totalfactura = 0
    facturafin = 0
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    if pk_token != "0":
        pk_desencriptado = desencriptar_datos2(pk_token,request)
        cajaapertc = cajaapertcierre.objects.filter(idcajaapertcierre=pk_desencriptado)  # Recuperar la compra por su clave primaria
    else:
        cajaapertc = cajaapertcierre.objects.filter(idempresa=didempresa, idsucursal=didsucursal,facturafin='')

    facturaini = ([detalle.facturaini for detalle in cajaapertc])[0]

    qs = Ventacab.objects.filter(idempresa=didempresa, idsucursal=didsucursal,nrofactura__gte=facturaini)
    totalfactura = sum([detalle.total for detalle in qs])

    qs = seriedet.objects.filter(idserie=1,iddocumentos=1,idempresa=didempresa,idsucursal=didsucursal)
    facturafin = ([detalle.correlativa for detalle in qs])[0]
    facturafin=int(facturafin)-1
    if int(facturaini) > int(facturafin):
        facturafin = 0
        facturaini = 0

    for objeto in cajaapertc:
        objeto.totalfactura = totalfactura
        objeto.facturafin = facturafin
        objeto.facturaini = facturaini
        objeto.save()

    return redirect('cajaapcierre_cargar', pk_token=str(0))


def cajaapcierredet_listar(request):
    if not request.user.has_perm('caja.view_cajaapertcierredet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    idcajaapertcierre = request.POST['pkf']

    skey = iskey(request)
    idcajaapertcierre = desencriptar_datos2(idcajaapertcierre,request)
    objetos = cajaapertcierredet.objects.filter(idcajaapertcierre=idcajaapertcierre).order_by('-tipo')
    cajaapertc = cajaapertcierre.objects.filter(idcajaapertcierre=idcajaapertcierre)
    facturaini = ([detalle.facturaini for detalle in cajaapertc])[0]

    ventas = Ventacab.objects.filter(idempresa=didempresa, idsucursal=didsucursal, nrofactura__gte=facturaini)
    ids_ventas = [venta.idventacab for venta in ventas]

    #ventas_agrupadas = cajaventapago.objects.values('formapago').annotate(total_monto=Sum('monto'))
    #ventas_agrupadas = cajaventapago.objects.filter(idventacab=ids_ventas).values('formapago').annotate(
     #   total_monto=Sum('monto'))

    ventas_agrupadas = cajaventapago.objects.filter(idventacab__in=ids_ventas).values('formapago').annotate(
        total_monto=Sum('monto'))

    datos = []

    for pagos in ventas_agrupadas:
        datos.append({
            'pkfd': encriptar_datos2(0, request),
            'tipomov': pagos['formapago'],
            'monto': f"{(pagos['total_monto']):.0f}",
            'tipo': 'ingreso',
        })

    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos2(objeto.idcajaapertcierredet,request),
            'tipomov': objeto.tipomov,
            'monto': f"{(objeto.monto):.0f}",
            'tipo': objeto.tipo,
        })

    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response

def cajaapcierredet_guardar(request):
    if not request.user.has_perm('caja.add_cajaapertcierredet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    if request.method == 'POST':

        pkf = request.POST['pkf']
        tipomov = request.POST['tipomov']
        monto = request.POST['monto']
        tipo = request.POST['tipo']

        idcajaapertcierre = desencriptar_datos2(pkf, request)


        obs = cajaapertcierredet()
        obs.idcajaapertcierre = float(idcajaapertcierre)
        obs.tipomov = tipomov
        obs.monto = monto
        obs.tipo = tipo
        obs.idempresa=didempresa
        obs.idsucursal=didsucursal
        obs.save()
        response = {'success': True}
        return JsonResponse(response)


def cajaapcierredet_eliminar(request,pk_token):
    if not request.user.has_perm('caja.delete_cajaapertcierredet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    skey = iskey(request)
    idcajaapertcierredet = desencriptar_datos2(pk_token,request)
    objetos = cajaapertcierredet.objects.filter(idcajaapertcierredet=idcajaapertcierredet)
    objetos.delete()
    response = {'success': True}
    return JsonResponse(response)
