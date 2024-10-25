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
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum



def presupuestocompcab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'compras/presupuestocompra_filt.html')

def presupuestocompcab_filtro_lst(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idproveedor =  request.GET.get('idproveedor', '')
    fechaini =  request.GET.get('fechaini', '')
    fechafin =  request.GET.get('fechafin', '')
    tipodoc =  request.GET.get('tipodoc', '')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

       
    presupuestocompcab = Presupuestocompcab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)

    if idproveedor=='':
        idproveedor=0
    if presupuestocompcab.exists() and int(idproveedor) >=1:
            presupuestocompcab = presupuestocompcab.filter(idproveedor_id=idproveedor,idempresa=didempresa,idsucursal=didsucursal)
    if presupuestocompcab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            presupuestocompcab = presupuestocompcab.filter(fecha__gte=fecha_inicio,idempresa=didempresa,idsucursal=didsucursal)
    if presupuestocompcab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            presupuestocompcab = presupuestocompcab.filter(fecha__lte=fecha_fin,idempresa=didempresa,idsucursal=didsucursal)
    if presupuestocompcab.exists() and tipodoc:
        presupuestocompcab = presupuestocompcab.filter(tipodoc=tipodoc,idempresa=didempresa,idsucursal=didsucursal)
    skey = iskey(request)
    for objeto in presupuestocompcab:
        objeto.pkpc = encriptar_datos(objeto.idpresupuestocompcab,skey)

    cadena=""
    return render(request, 'compras/presupdecompra_lst.html', {'presupuestocompcab': presupuestocompcab, 'cadena': cadena })


def presupuestocompcab_listar(request,cadena):
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

       
    if cadena == "*":
        presupuestocompcab = Presupuestocompcab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'compras/presupdecompra_lst.html', {'presupuestocompcab': presupuestocompcab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'compras/presupdecompra_lst.html')

    qs = Presupuestocompcab.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Presupuestocompcab.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Presupuestocompcab.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Presupuestocompcab.objects.filter(proveedor__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Presupuestocompcab.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    presupuestocompcab = qs
    return render(request, 'compras/presupdecompra_lst.html', {'presupuestocompcab': presupuestocompcab, 'cadena': cadena})

class presupuestocompcab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_presupuestocompcab'
    model = Presupuestocompcab
    form_class = PresupuestodecompcabForm
    template_name = 'compras/presupdecompra.html'
    success_url = reverse_lazy('presupuestocompcab_crear')

    def get(self, request,pk_token):
        presupuestocompcab = None
        if pk_token != "0":
            skey = iskey(request)
            pk_desencriptado = desencriptar_datos(pk_token,skey)
            presupuestocompcab = Presupuestocompcab.objects.get(idpresupuestocompcab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'presupuestocompcab': presupuestocompcab}  # Crear un diccionario de contexto
        context['title'] = '  PRESUPUESTO - COMPRA  '
        context['sidr'] = '/presupuestocompcab/' + str(pk_token) + '/cargar/'
        context['pkpc'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False

        return render(request, self.template_name, context)


class presupuestocompcab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_presupuestocompcab'
    model = Presupuestocompcab
    form_class = PresupuestodecompcabForm
    template_name = 'compras/presupdecompra.html'
    success_url = reverse_lazy('presupuestocompcab_crear')

    def dispatch(self, *args, **kwargs):
        return super(presupuestocompcab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'PRESUPUESTO DE COMPRA '
        context['sidr'] = '/presupuestocompcab/crear/'
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self,request, form):
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')



        Presupuestocompcab = form.save(commit=False)
        Presupuestocompcab.idempresa = idempresa
        Presupuestocompcab.idsucursal = idsucursal
        Presupuestocompcab.save()

        messages.success(self.request, ' registro creado exitosamente.')
        skey = iskey(request)
        pk_encriptado = encriptar_dato(self.object.pk,skey)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('presupuestocompcab_cargar', pk_token=pk_encriptado)

class presupuestocompcab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_compracab'
    model = Presupuestocompcab
    form_class = PresupuestodecompcabForm
    template_name = 'compras/presupdecompra.html'
    success_url = reverse_lazy('presupuestocompcab_crear')

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']

        if pk_token != "0":
            skey = iskey(self.request)
            pk = desencriptar_datos(pk_token,skey)
            return get_object_or_404(Presupuestocompcab, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR PRESUPUESTO  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/presupuestocompcab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkpc'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        compracab = self.object
        messages.success(self.request, ' editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('presupuestocompcab_cargar', kwargs={'pk_token': pk_token})


class presupuestocompcab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_presupuestocompcab'

    def get(self, request, pk_token):
        pk = desencriptar_dato(pk_token)
        instance = get_object_or_404(Presupuestocompcab, pk=pk)
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            pk = desencriptar_dato(pk_token)
            instance = get_object_or_404(Presupuestocompcab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, ' eliminado exitosamente.')
            return redirect('presupuestocompcab_cargar', pk_token=0)
        else:
            return redirect('presupuestocompcab_cargar', pk_token=pk_token)

def presupuestocompdet_listar(request):
    if not request.user.has_perm('compras.view_presupuestocompdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pkpc = request.POST['pkpc']
    idpresupuestocompcab = int(desencriptar_dato(pkpc))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Presupuestocompdet.objects.filter(idpresupuestocompcab=idpresupuestocompcab).order_by('orden')
    if int(orden) >=1:
        objetos = Presupuestocompdet.objects.filter(idpresupuestocompcab=idpresupuestocompcab,orden=orden)
    datos = []
    print(" idpresupuestocompcab " + str(idpresupuestocompcab))

    for objeto in objetos:
        datos.append({
            'pkpcd': encriptar_dato(objeto.idpresupuestocompdet),
            'orden': objeto.orden,
            'codigo': objeto.codigo,
            'descripcion': objeto.descripcion,
            'cantidad': objeto.cantidad,
            'precio': f"{(objeto.precio):.0f}",
            'iva': f"{(objeto.iva):.0f}",
            'subtotal': f"{(objeto.precio * objeto.cantidad):.0f}"
             })

    Response = JsonResponse({'datos': datos,'success': True, 'message': ''})
    return Response


def actpresupuestocompracab(idpresupuestocompcab):

    detalles = Presupuestocompdet.objects.filter(iva=5,idpresupuestocompcab=idpresupuestocompcab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Presupuestocompdet.objects.filter(iva=10, idpresupuestocompcab=idpresupuestocompcab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Presupuestocompdet.objects.filter(iva=0, idpresupuestocompcab=idpresupuestocompcab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Presupuestocompcab.objects.filter(idpresupuestocompcab=idpresupuestocompcab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def presupuestocompdet_guardar(request):
    if not request.user.has_perm('compras.add_presupuestocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':

        pkpc = request.POST['pkpc']
        idpresupuestocompcab = desencriptar_dato(pkpc)

    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Presupuestocompdet.objects.filter(idpresupuestocompcab=idpresupuestocompcab).count()
        cantr=cantr+1

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            presupuestocompdet = Presupuestocompdet()
            presupuestocompdet.idpresupuestocompcab =float(idpresupuestocompcab)
            presupuestocompdet.orden = cantr
            presupuestocompdet.idarticulo = articulo.idarticulo
            presupuestocompdet.codigo =  articulo.codigo
            presupuestocompdet.descripcion = articulo.descripcion
            presupuestocompdet.cantidad = float(cantidad)
            presupuestocompdet.unidad = articulo.unidad
            presupuestocompdet.costo =articulo.costo
            presupuestocompdet.precio = float(precio)
            presupuestocompdet.iva = articulo.iva
            Presupuestocompcab.idempresa = idempresa
            Presupuestocompcab.idsucursal = idsucursal
            presupuestocompdet.save()
            actpresupuestocompracab(idpresupuestocompcab)
            response = {'success': True}
            return JsonResponse(response)

def presupuestocompdet_editar(request):

    if not request.user.has_perm('compras.change_presupuestocompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkpc = request.POST['pkpc']
        idpresupuestocompcab = desencriptar_dato(pkpc)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Presupuestocompdet.objects.filter(idpresupuestocompcab=idpresupuestocompcab,orden=orden)
        for presupuestocompdet in objetos:
            idpresupuestocompdet=presupuestocompdet.idpresupuestocompdet

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            presupuestocompdet = get_object_or_404(Presupuestocompdet, pk=idpresupuestocompdet)
            presupuestocompdet.idcompracab =float(idpresupuestocompcab)
            presupuestocompdet.orden = orden
            presupuestocompdet.idarticulo = articulo.idarticulo
            presupuestocompdet.codigo =  articulo.codigo
            presupuestocompdet.descripcion = articulo.descripcion
            presupuestocompdet.cantidad = float(cantidad)
            presupuestocompdet.unidad = articulo.unidad
            presupuestocompdet.costo =articulo.costo
            presupuestocompdet.precio = float(precio)
            presupuestocompdet.iva = articulo.iva
            presupuestocompdet.save()
            actpresupuestocompracab(idpresupuestocompcab)
            response = {'success': True}
            return JsonResponse(response)


def presupuestocompdet_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_compradet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)
    pk = int(desencriptar_dato(pk_token))
    objetos = Presupuestocompdet.objects.filter(idpresupuestocompdet=pk)

    for objeto in objetos:
        idpresupuestocompcab= objeto.idpresupuestocompcab

    presupuestocompdet = get_object_or_404(Presupuestocompdet, idpresupuestocompdet=pk)
    presupuestocompdet.delete()

    orden=0
    objetos = Presupuestocompdet.objects.filter(idpresupuestocompcab=idpresupuestocompcab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actpresupuestocompracab(idpresupuestocompcab)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)
