from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from contabilidad.forms import AsientoForm
from contabilidad.models import asiento, asiento_det
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from django.contrib import messages
from django.utils import timezone
from contabilidad.models import Cuentacontable

# Create your views here.


def asiento_filtar(request):
    if request.user.is_authenticated:
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')
        return render(request, 'contabilidad/asiento_listar.html')
    else:
        return redirect('login')


def asiento_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


    if cadena == "*"  or cadena == "0" or cadena == "":

        iasiento = asiento.objects.filter(idempresa=didempresa)
        for objeto in iasiento:
            objeto.pkas = encriptar_datos2(objeto.idasiento,request)
            objeto.debe = "{:,.0f}".format(float(objeto.debe))
            objeto.haber = "{:,.0f}".format(float(objeto.haber))

        return render(request, 'contabilidad/asiento_listar.html', {'asiento': iasiento, 'cadena': '' })

    qs = asiento.objects.filter(idempresa=didempresa ,cuenta='')
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
            objeto.pkas = encriptar_datos2(objeto.idasiento,request)
            objeto.debe = "{:,.0f}".format(float(objeto.debe))
            objeto.haber = "{:,.0f}".format(float(objeto.haber))

    return render(request, 'contabilidad/asiento_listar.html', {'asiento': icasiento ,'cadena': cadena})



class asiento_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_asiento'
    model = asiento
    form_class = AsientoForm
    template_name = 'contabilidad/asiento.html'
    context_object_name = 'asiento'  # Nombre para acceder al objeto en la plantilla

    def get(self, request, pk_token):
        kasiento = None
        kasiento_det = None
        cueta_cont_list = None

        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        ctacontable = obtenercuentacont(didempresa, request)
        if ctacontable:
            didcuenta = ctacontable[0]['idcuenta']
            denominacion = ctacontable[0]['denominacion']
            idcuenta = desencriptar_datos2(str(didcuenta), request)
        cueta_cont_list=ctacontable

        if pk_token != "0":

            pk_desencriptado = desencriptar_datos2(pk_token,request)

            kasiento = asiento.objects.get(idasiento=int(pk_desencriptado))

            # Formatear debe y haber si no es None
            kasiento.debe = "{:,.0f}".format(float(kasiento.debe)) if kasiento.debe else 0
            kasiento.haber = "{:,.0f}".format(float(kasiento.haber)) if kasiento.haber else 0

            kasiento_det = asiento_det.objects.filter(idasiento=int(pk_desencriptado)).order_by('orden')
            for objeto in kasiento_det:
                objeto.pkasdet = encriptar_datos2(objeto.idasientodet, request)
                objeto.debe = "{:,.0f}".format(float(objeto.debe))
                objeto.haber = "{:,.0f}".format(float(objeto.haber))


        context = {'asiento': kasiento,'asiento_det': kasiento_det,'cueta_cont_list':cueta_cont_list}  # Crear un diccionario de contexto
        context['title'] = '  ASIENTO  '
        context['sidr'] = '/asiento/' + str(pk_token) + '/cargar/'
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False
        return render(request, self.template_name, context)


def lista_cuenta(didempresa, didsucursal):
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')
    ctacont = Cuentacontable.objects.filter(idempresa=didempresa)  # Asegúrate de que `idcompracab` sea un entero
    for dato in object:
        idcuenta = ctacont.idcuentacontable
        denominacion = ctacont.denominacion

    return dato

def obtenercuentacont(didempresa,request):
    ctacontable = []
    objetos = Cuentacontable.objects.filter(asentable='SI',idempresa=didempresa)
    i = 0
    cantr = objetos.count()
    for objeto in objetos:
        if i == 0:
            idcuenta=objeto.idcuentacontable
            denominacion=objeto.denominacion
            i=1

        ctacontable.append({
            'idcuenta': encriptar_datos2(str(objeto.idcuentacontable),request),
            'denominacion': objeto.denominacion,
        })


    return ctacontable



class asiento_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'contabilidad.add_asiento'
    model = asiento
    form_class = AsientoForm
    template_name = 'contabilidad/asiento.html'
    success_url = reverse_lazy('asiento_crear')

    def dispatch(self, *args, **kwargs):
        return super(asiento_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = '  CREAR  ASIENTO '
        context['sidr'] = '/asiento/crear/'

        context['hab1']= False
        context['hab2']= True

        return context
    def form_valid(self, form):


        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')
        asiento = form.save(commit=False)
        asiento.idempresa = didempresa
        asiento.idsucursal = didsucursal
        asiento.fecha_hora = timezone.now()  # Asigna la fecha y hora actual correctamente
        asiento.save()

        response = super().form_valid(form)
        messages.success(self.request, 'asiento creado exitosamente.')
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('asiento_cargar', pk_token=str(pk_encriptado))


class asiento_editar(LoginRequiredMixin, ValidarPermisoMixin, UpdateView):
    permission_required = 'contabiliad.chance_asiento'
    model = asiento
    form_class = AsientoForm
    template_name = 'contabilidad/asiento.html'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            return get_object_or_404(asiento, pk=pk)

    def get_context_data(self, **kwargs):
        idempresa = self.request.session['idempresa']
        idsucursal = self.request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pk_token = self.kwargs['pk_token']
        kasiento=None
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            kasiento = asiento.objects.get(idasiento=int(pk))

        context = super().get_context_data(**kwargs)
        context['title'] = 'EDITAR CUENTA'
        pk_token = self.kwargs['pk_token']
        context['asiento'] = kasiento

        context['sidr'] = '/asiento/' + str(pk_token) + '/editar/'
        context['pk_token'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context


    def get_success_url(self):
        messages.success(self.request, 'asiento editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('asiento_cargar', kwargs={'pk_token': pk_token})


class asiento_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'contabilidad.delete_asiento'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')
        pk = desencriptar_datos2(pk_token,request)


        if asiento_det.objects.filter(idasiento=pk).exclude(idcuentacontable=pk).exists():
            messages.error(self.request, 'Tiene detalles asociados .')
            return redirect('asiento_cargar', pk_token=pk_token)


        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        if pk_token =="0":
            return redirect('asiento_cargar', pk_token=0)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(asiento, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'asiento eliminada exitosamente.')
            return redirect('asiento_cargar', pk_token=0)
        else:
            return redirect('asiento_cargar', pk_token=str(pk_token))




def asiento_det_crear(request):
    if request.method == 'POST':
        # Recoge los datos enviados por AJAX
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pk_token = request.POST.get('pk_token')

        cuenta = request.POST.get('cuenta')
        denominacion = request.POST.get('denominacion')
        debe = request.POST.get('debe')
        haber = request.POST.get('haber')
        decimal=0
        debe=contorlnumerico(debe, decimal)
        haber=contorlnumerico(haber, decimal)

        if debe == 0 and haber == 0:
            return JsonResponse({'message': 'Debe o haber no puede ser cero.'}, status=400)

        icuenta=""
        ictacontable = Cuentacontable.objects.filter(cuenta=cuenta,idempresa=didempresa)
        for objeto in ictacontable:
            didctacontable = objeto.idcuentacontable
            icuenta = objeto.cuenta
        if cuenta != icuenta:
            return JsonResponse({'message': 'cuenta no coincide'}, status=400)

        pk = desencriptar_datos2(pk_token, request)

        asiento_instance = asiento.objects.get(pk=int(pk))  # Asegúrate de que `idcompracab` sea un entero
        ctacont_instance = Cuentacontable.objects.get(pk=int(didctacontable))  # Asegúrate de que `idcompracab` sea un entero
        cantr = asiento_det.objects.filter(idasiento=pk).count()
        cantr=cantr+1
        # Aquí deberías obtener el objeto del detalle del asiento a actualizar
        asiento_detalle = asiento_det()
        # Actualiza los campos
        asiento_detalle.orden = cantr
        asiento_detalle.idasiento=asiento_instance
        asiento_detalle.idcuentacontable=ctacont_instance
        asiento_detalle.cuenta = cuenta
        asiento_detalle.denominacion = denominacion
        asiento_detalle.debe = debe
        asiento_detalle.haber = haber
        asiento_detalle.fecha = timezone.now()
        asiento_detalle.fecha_hora = timezone.now()
        asiento_detalle.idempresa = didempresa
        asiento_detalle.idsucursal = didsucursal
        asiento_detalle.save()
        actualizattotasiento(pk)

        #return redirect('asiento_cargar', pk_token=str(pk_token))
        return JsonResponse({'message': 'Detalle actualizado correctamente.'})

def actualizattotasiento(didasiento):
    detalles = asiento_det.objects.filter(idasiento=didasiento)
    debe = sum([detalle.debe for detalle in detalles])
    haber = sum([detalle.haber for detalle in detalles])

    objetos = asiento.objects.filter(idasiento=didasiento)
    for objeto in objetos:
        objeto.debe = debe
        objeto.haber = haber
        objeto.save()


def asiento_det_actualizar(request):
    if request.method == 'POST':
        # Recoge los datos enviados por AJAX
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pk_token = request.POST.get('pk_token')
        pk_token_det = request.POST.get('pk_token_det')
        cuenta = request.POST.get('cuenta')
        denominacion = request.POST.get('denominacion')
        debe = request.POST.get('debe')
        haber = request.POST.get('haber')
        decimal=0
        debe=contorlnumerico(debe, decimal)
        haber=contorlnumerico(haber, decimal)
        if debe == 0 and haber == 0:
            return JsonResponse({'message': 'Debe o haber no puede ser cero.'}, status=400)
        icuenta=""
        ictacontable = Cuentacontable.objects.filter(cuenta=cuenta,idempresa=didempresa)
        for objeto in ictacontable:
            didctacontable = objeto.idcuentacontable
            icuenta = objeto.cuenta

        if cuenta != icuenta:
            return JsonResponse({'message': 'cuenta no coincide'}, status=400)

        pk = desencriptar_datos2(pk_token, request)
        pk_det = desencriptar_datos2(pk_token_det, request)
        ctacont_instance = Cuentacontable.objects.get(pk=int(didctacontable))  # Asegúrate de que `idcompracab` sea un entero
        # Aquí deberías obtener el objeto del detalle del asiento a actualizar
        asiento_detalle = get_object_or_404(asiento_det, pk=pk_det)
        # Actualiza los campos
        asiento_detalle.idcuentacontable = ctacont_instance
        asiento_detalle.cuenta = cuenta
        asiento_detalle.denominacion = denominacion
        asiento_detalle.debe = debe
        asiento_detalle.haber = haber
        asiento_detalle.fecha = timezone.now()
        asiento_detalle.fecha_hora = timezone.now()
        asiento_detalle.save()
        actualizattotasiento(pk)

        return JsonResponse({'message': 'Detalle actualizado correctamente.'})


class asiento_det_eliminar(LoginRequiredMixin, ValidarPermisoMixin, View):
    permission_required = 'contabilidad.delete_asiento_det'
    pk_token_did=''
    def get(self, request, pk_token):

        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        pk = desencriptar_datos2(pk_token, self.request)
        objeto_det = asiento_det.objects.filter(pk=pk)
        for objeto in objeto_det:
            didasiento = objeto.idasiento_id
            pk_token_did = encriptar_datos2(str(didasiento), self.request)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,self.request)
            instance = get_object_or_404(asiento_det, pk=pk)


            try:
                instance.delete()
                iorden = 0
                objetos = asiento_det.objects.filter(idasiento=didasiento).order_by('orden')
                for objeto in objetos:
                    iorden = iorden + 1
                    objeto.orden = int(iorden)
                    objeto.save()
                actualizattotasiento(didasiento)

            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'asiento det eliminado exitosamente.')
            return redirect('asiento_cargar', pk_token=str(pk_token_did))
        else:
            return redirect('asiento_cargar', pk_token=str(pk_token_did))


def contorlnumerico(numero,decimal):
    valor=numero
    try:
        float(numero)  # Si puede ser convertida a float, es numérica
    except ValueError:
        valor = 0
    return  valor

def bucardenominacion(request):
    if request.method == 'POST':
        dato=""
        # Recoge los datos enviados por AJAX
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        cuenta = request.POST.get('cuenta')
        ictacontable = Cuentacontable.objects.filter(idempresa=didempresa,cuenta=cuenta)
        if ictacontable.exists():
            for objeto in ictacontable:
                idcuenta = objeto.idcuentacontable
                dato = objeto.denominacion

        return JsonResponse({'denominacion': dato}, status=200)


def buscarcuentalist(request):
    if request.method == 'POST':
        # Recoge los datos enviados por AJAX
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        id = request.POST.get('id')
        did = desencriptar_datos2(id, request)
        ictacontable = Cuentacontable.objects.filter(idcuentacontable=did)
        if not ictacontable.exists():
            Response = JsonResponse({'datos': None, 'success': True, 'message': ''})
            return Response

        datos = []
        if ictacontable.exists():
            for objeto in ictacontable:
                datos.append({
                    'pkcta': encriptar_datos2(objeto.idcuentacontable, request),
                    'cuenta': objeto.cuenta,
                    'denominacion': objeto.denominacion,
                })
            print(' buscarcuenta '+str(datos))
            # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
            Response = JsonResponse({'datos': datos, 'success': True, 'message': ''})
            return Response

