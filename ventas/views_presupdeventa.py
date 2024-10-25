from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from compras.forms import *
from compras.forms import *

from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum



def presupuestoventacab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'ventas/presupuestoventa_filt.html')

def presupuestoventacab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idcliente =  request.GET.get('idcliente', '')
    fechaini =  request.GET.get('fechaini', '')
    fechafin =  request.GET.get('fechafin', '')
    tipodoc =  request.GET.get('tipodoc', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')
    presupuestoventacab = Presupuestoventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)

    if idcliente=='':
        idcliente=0
    if presupuestoventacab.exists() and int(idcliente) >=1:
            presupuestoventacab = presupuestoventacab.filter(idcliente_id=idcliente)
    if presupuestoventacab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            presupuestoventacab = presupuestoventacab.filter(fecha__gte=fecha_inicio)
    if presupuestoventacab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            presupuestoventacab = presupuestoventacab.filter(fecha__lte=fecha_fin)
    if presupuestoventacab.exists() and tipodoc:
        presupuestoventacab = presupuestoventacab.filter(tipodoc=tipodoc)
    skey = iskey(request)
    for objeto in presupuestoventacab:
        objeto.pkpv = encriptar_datos2(objeto.idpresupuestoventacab,request)

    cadena=""
    return render(request, 'ventas/presupdeventa_lst.html', {'presupuestoventacab': presupuestoventacab, 'cadena': cadena })


def presupuestoventacab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if cadena == "*":
        print("valor"+ cadena)
        presupuestoventacab = Presupuestoventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'ventas/presupdeventa_lst.html', {'presupuestoventacab': presupuestoventacab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/presupdeventa_lst.html')

    qs = Presupuestoventacab.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Presupuestoventacab.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Presupuestoventacab.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Presupuestoventacab.objects.filter(cliente__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Presupuestoventacab.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    presupuestoventacab = qs
    return render(request, 'ventas/presupdeventa_lst.html', {'presupuestoventacab': presupuestoventacab, 'cadena': cadena})

class presupuestoventacab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_presupuestoventacab'
    model = Presupuestoventacab
    form_class = PresupuestoventacabForm
    template_name = 'ventas/presupdeventa.html'
    success_url = reverse_lazy('presupuestoventacab_cargar')

    def get(self, request,pk_token):
        presupuestoventacab = None
        if pk_token != "0":
            skey = iskey(request)
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            presupuestoventacab = Presupuestoventacab.objects.get(idpresupuestoventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'presupuestoventacab': presupuestoventacab}  # Crear un diccionario de contexto
        context['title'] = '  PRESUPUESTO - VENTA  '
        context['sidr'] = '/Presupuestoventacab/' + str(pk_token) + '/cargar/'
        context['pkpv'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class presupuestoventacab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_presupuestoventacab'

    model = Presupuestoventacab
    form_class = PresupuestoventacabForm
    template_name = 'ventas/presupdeventa.html'
    success_url = reverse_lazy('presupuestoventacab_crear')

    def dispatch(self, *args, **kwargs):
        return super(presupuestoventacab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'PRESUPUESTO DE VENTA '
        context['sidr'] = '/presupuestoventacab/crear/'
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        Presupuestoventacab = form.save(commit=False)
        Presupuestoventacab.idempresa = didempresa
        Presupuestoventacab.idsucursal = didsucursal
        Presupuestoventacab.save()

        response = super().form_valid(form)
        messages.success(self.request, 'presuspuesto  creado exitosamente.')
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('presupuestoventacab_cargar', pk_token=pk_encriptado)

class presupuestoventacab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'ventas.change_presupuestoventacab'
    model = Presupuestoventacab
    form_class = PresupuestoventacabForm
    template_name = 'ventas/presupdeventa.html'
    success_url = '/presupuestoventacab/0/listar/'


    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = iskey(self.request)
            pk = desencriptar_datos2(pk_token,self.request)

            return get_object_or_404(Presupuestoventacab, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR PRESUPUESTO  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/presupuestoventacab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        compracab = self.object
        messages.success(self.request, ' presupuesto editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        #return reverse_lazy('compracab_editar', kwargs={'pk_token': pk_encriptado})
        return reverse_lazy('presupuestoventacab_cargar', kwargs={'pk_token': pk_token})


class presupuestoventacab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_presupuestoventacab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE PRESUPUESTO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        if pk_token =="0":
            return redirect('presupuestoventacab_cargar', pk_token=0)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,request)

            instance = get_object_or_404(Presupuestoventacab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')
            return redirect('presupuestoventacab_cargar', pk_token=0)
        else:
            return redirect('presupuestoventacab_cargar', pk_token=pk_token)


def presupuestoventadet_listar(request):
    if not request.user.has_perm('ventas.view_presupuestoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['pkpv']
    skey = iskey(request)
    idpresupuestoventacab = int(desencriptar_datos2(pk,request))
    orden = request.POST['orden']
    if int(orden) == 0:
        objetos = Presupuestoventadet.objects.filter(idpresupuestoventacab=idpresupuestoventacab).order_by('orden')
    if int(orden) >=1:
        objetos = Presupuestoventadet.objects.filter(idpresupuestoventacab=idpresupuestoventacab,orden=orden)
    datos = []
    skey = iskey(request)
    for objeto in objetos:
        datos.append({
            'pkpvd': encriptar_datos2(objeto.idpresupuestoventadet,request),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
        })


    # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def actpresupuestoventacab(idpresupuestoventacab):

    detalles = Presupuestoventadet.objects.filter(iva=5,idpresupuestoventacab=idpresupuestoventacab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Presupuestoventadet.objects.filter(iva=10, idpresupuestoventacab=idpresupuestoventacab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Presupuestoventadet.objects.filter(iva=0, idpresupuestoventacab=idpresupuestoventacab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta
    print(str(idpresupuestoventacab))
    objetos = Presupuestoventacab.objects.filter(idpresupuestoventacab=idpresupuestoventacab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def presupuestoventadet_guardar(request):
    if not request.user.has_perm('ventas.add_presupuestoventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)


    if request.method == 'POST':
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pkpv= request.POST['pkpv']
        idpresupuestoventacab = desencriptar_datos2(pkpv,request)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Presupuestoventadet.objects.filter(idpresupuestoventacab=idpresupuestoventacab).count()
        cantr=cantr+1
        presupventa_instance = Presupuestoventacab.objects.get(pk=int(idpresupuestoventacab))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(
                pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            presupuestoventadet = Presupuestoventadet()
            presupuestoventadet.idpresupuestoventacab =presupventa_instance
            presupuestoventadet.orden = cantr
            presupuestoventadet.idarticulo = articulo_instance
            presupuestoventadet.codigo =  articulo.codigo
            presupuestoventadet.descripcion = articulo.descripcion
            presupuestoventadet.cantidad = float(cantidad)
            presupuestoventadet.unidad = articulo.unidad
            presupuestoventadet.costo =articulo.costo
            presupuestoventadet.precio = float(precio)
            presupuestoventadet.iva = articulo.iva
            presupuestoventadet.save()
            actpresupuestoventacab(idpresupuestoventacab)
            response = {'success': True}
            return JsonResponse(response)

def presupuestoventadet_editar(request):
    if not request.user.has_perm('ventas.change_presupuestoventadet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        pkpv = request.POST['pkpv']
        skey = iskey(request)
        idpresupuestoventacab = int(desencriptar_datos2(pkpv,request))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Presupuestoventadet.objects.filter(idpresupuestoventacab=idpresupuestoventacab,orden=orden)
        for presupuestoventadet in objetos:
            idpresupuestoventadet=presupuestoventadet.idpresupuestoventadet

        presupventa_instance = Presupuestoventacab.objects.get(pk=int(idpresupuestoventacab))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(
                pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            presupuestoventadet = get_object_or_404(Presupuestoventadet, pk=idpresupuestoventadet)
            presupuestoventadet.idpresupuestoventacab =presupventa_instance
            presupuestoventadet.orden = orden
            presupuestoventadet.idarticulo = articulo_instance
            presupuestoventadet.codigo =  articulo.codigo
            presupuestoventadet.descripcion = articulo.descripcion
            presupuestoventadet.cantidad = float(cantidad)
            presupuestoventadet.unidad = articulo.unidad
            presupuestoventadet.costo =articulo.costo
            presupuestoventadet.precio = float(precio)
            presupuestoventadet.iva = articulo.iva
            presupuestoventadet.idempresa=didempresa
            presupuestoventadet.idsucursal=didsucursal
            presupuestoventadet.save()
            actpresupuestoventacab(idpresupuestoventacab)
            response = {'success': True}
            return JsonResponse(response)


def presupuestoventadet_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_presupuestoventadet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

    pk = int(desencriptar_datos2(pk_token,request))


    presupventadet_instance = Presupuestoventadet.objects.get(pk=pk)
    idpresupuestoventacab = presupventadet_instance.idpresupuestoventacab_id
    print(idpresupuestoventacab)

    presupuestoventadet = get_object_or_404(Presupuestoventadet, idpresupuestoventadet=pk)
    presupuestoventadet.delete()

    orden=0
    objetos = Presupuestoventadet.objects.filter(idpresupuestoventacab=idpresupuestoventacab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actpresupuestoventacab(idpresupuestoventacab)

    response = {'success': True, 'message': ''}
    return JsonResponse(response)
