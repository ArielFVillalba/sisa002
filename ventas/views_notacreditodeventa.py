from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import datetime
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.datetime_safe import datetime


from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from stock.models import Deposito
from .forms import *
from compras.forms import *

from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum

from stock.views import actualizarexistencia, verificardepostio
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver


def notacreditoventacab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'ventas/notacreditoventa_filt.html')

def notacreditoventacab_filtro_lst(request):
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

    notacreditoventacab = Notacreditoventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)

    if idcliente=='':
       idcliente=0
    if notacreditoventacab.exists() and int(idcliente) >=1:
       notacreditoventacab = notacreditoventacab.filter(idcliente_id=idcliente,idempresa=didempresa,idsucursal=didsucursal)
    if notacreditoventacab.exists() and fechaini:
       fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
       notacreditoventacab = notacreditoventacab.filter(fecha__gte=fecha_inicio,idempresa=didempresa,idsucursal=didsucursal)
    if notacreditoventacab.exists() and fechafin:
       fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
       notacreditoventacab = notacreditoventacab.filter(fecha__lte=fecha_fin,idempresa=didempresa,idsucursal=didsucursal)
    if notacreditoventacab.exists() and tipodoc:
       notacreditoventacab = notacreditoventacab.filter(tipodoc=tipodoc,idempresa=didempresa,idsucursal=didsucursal)

    skey = iskey(request)

    for objeto in notacreditoventacab:
        objeto.pknc = encriptar_datos2(objeto.idnotacreditoventacab,request)

    cadena=""
    return render(request, 'ventas/notacreditoventa_lst.html', {'notacreditoventacab': notacreditoventacab, 'cadena': cadena })


def notacreditoventacab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

    if cadena == "*":
        notacreditoventacab = Notacreditoventacab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'ventas/notacreditoventa_lst.html', {'notacreditoventacab': notacreditoventacab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/notacreditoventa_lst.html')

    qs = Notacreditoventacab.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Notacreditoventacab.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Notacreditoventacab.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Notacreditoventacab.objects.filter(proveedor__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Notacreditoventacab.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    notacreditoventacab = qs
    return render(request, 'ventas/notacreditodeventara_lst.html', {'notacreditoventacab': notacreditoventacab, 'cadena': cadena})


class notacreditoventacab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_notacreditoventacab'
    model = Notacreditoventacab
    form_class = NotacreditoventacabForm
    template_name = 'ventas/notacreditoventa.html'
    success_url = reverse_lazy('notacreditoventacab_cargar')

    def get(self, request,pk_token):
        notacreditoventacab = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,self.request)
            notacreditoventacab = Notacreditoventacab.objects.get(idnotacreditoventacab=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'notacreditoventacab': notacreditoventacab}  # Crear un diccionario de contexto
        context['title'] = '   NOTA CREDITO - VENTA  '
        context['sidr'] = '/notacreditoventacab/' + str(pk_token) + '/cargar/'
        context['pknc'] = pk_token
        context['pk_token'] = pk_token
        context['hab1']= True
        context['hab2']= False
        return render(request, self.template_name, context)


class notacreditoventacab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_notacreditoventacab'

    model = Notacreditoventacab
    form_class = NotacreditoventacabForm
    template_name = 'ventas/notacreditoventa.html'
    success_url = reverse_lazy('notacreditoventacab_crear')
    def dispatch(self, *args, **kwargs):
        return super(notacreditoventacab_crear, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CREAR NOTA CREDITO DE VENTA '
        context['sidr'] = '/notacreditoventacab/crear/'
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

        Notacreditoventacab = form.save(commit=False)
        Notacreditoventacab.idempresa = didempresa
        Notacreditoventacab.idsucursal = didsucursal
        Notacreditoventacab.save()

        response = super().form_valid(form)
        messages.success(self.request, 'creado exitosamente.')
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('notacreditoventacab_cargar', pk_token=str(pk_encriptado))


class notacreditoventacab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'ventas.change_notacreditoventacab'

    model = Notacreditoventacab
    form_class = NotacreditoventacabForm
    template_name = 'ventas/notacreditoventa.html'
    success_url = '/notacreditoventacab/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(Notacreditoventacab, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NOTA CREDITO DE VENTA'
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/notacreditoventacab/'+str(pk_token)+'/editar/'
        context['pk_token'] = pk_token
        context['pknc'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return redirect('notacreditoventacab_cargar', pk_token=str(pk_token))

class notacreditoventacab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_ordencompcab'

    def get(self, request, pk_token):
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO  "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        if pk_token =="0":
            return redirect('notacreditoventacab_cargar', pk_token=0)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,self.request)
            instance = get_object_or_404(Notacreditoventacab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'eliminado exitosamente.')
            return redirect('notacreditoventacab_cargar', pk_token=0)
        else:
            return redirect('notacreditoventacab_cargar', pk_token=pk_token)


def notacreditoventadet_listar(request):
    if not request.user.has_perm('ventas.view_notacreditoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    idnotacreditoventacab = request.POST['pknc']
    idnotacreditoventacab = desencriptar_datos2(idnotacreditoventacab,request)

    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Notacreditoventadet.objects.filter(idnotacreditoventacab=idnotacreditoventacab).order_by('orden')
    if int(orden) >=1:
        objetos = Notacreditoventadet.objects.filter(idnotacreditoventacab=idnotacreditoventacab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkncd': encriptar_datos2(objeto.idnotacreditoventadet,request),
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


def actnotacreditoventacab(idnotacreditoventacab):

    #gravada10 = Compradet.objects.filter(iva=10,idventaracab=idventaracab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Notacreditoventadet.objects.filter(iva=5,idnotacreditoventacab=idnotacreditoventacab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notacreditoventadet.objects.filter(iva=10, idnotacreditoventacab=idnotacreditoventacab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Notacreditoventadet.objects.filter(iva=0, idnotacreditoventacab=idnotacreditoventacab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta

    objetos = Notacreditoventacab.objects.filter(idnotacreditoventacab=idnotacreditoventacab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total


def notacreditoventadet_guardar(request):
    if not request.user.has_perm('ventas.add_notacreditoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    if request.method == 'POST':
        idnotacreditoventacab = request.POST['pknc']
        idnotacreditoventacab = desencriptar_datos2(idnotacreditoventacab,request)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        deposito = request.POST['deposito']

        cantr = Notacreditoventadet.objects.filter(idnotacreditoventacab=idnotacreditoventacab).count()
        cantr=cantr+1

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)

        if verificardepostio(deposito, didempresa)==False:
            response = {'success': False, 'message': 'deposito invalido'}
            return JsonResponse(response)

        obj = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        scod = ([(detalle.codigo) for detalle in obj])[0] if obj else None
        if scod == None:
            response = {'success': False, 'message': 'codigo invalido'}
            return JsonResponse(response)

        notacreditoventacab_instance = Notacreditoventacab.objects.get(pk=int(idnotacreditoventacab))  # Asegúrate de que `idcompracab` sea un entero


        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            notacreditoventadet = Notacreditoventadet()
            notacreditoventadet.idnotacreditoventacab =notacreditoventacab_instance
            notacreditoventadet.orden = cantr
            notacreditoventadet.idarticulo = articulo_instance
            notacreditoventadet.codigo =  articulo.codigo
            notacreditoventadet.descripcion = articulo.descripcion
            notacreditoventadet.cantidad = float(cantidad)
            notacreditoventadet.unidad = articulo.unidad
            notacreditoventadet.costo =articulo.costo
            notacreditoventadet.precio = float(precio)
            notacreditoventadet.iva = articulo.iva
            notacreditoventadet.deposito = deposito
            notacreditoventadet.idempresa=didempresa
            notacreditoventadet.idsucursal=didsucursal
            notacreditoventadet.save()
            actnotacreditoventacab(idnotacreditoventacab)
            response = {'success': True}
            return JsonResponse(response)


def notacreditoventadet_editar(request):
    if not request.user.has_perm('ventas.add_notacreditoventadet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        idnotacreditoventacab = request.POST['pknc']
        idnotacreditoventacab = desencriptar_datos2(idnotacreditoventacab,request)
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Notacreditoventadet.objects.filter(idnotacreditoventacab=idnotacreditoventacab,orden=orden)
        for notacreditoventadet in objetos:
            idnotacreditoventadet=notacreditoventadet.idnotacreditoventadet

        obj = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        scod = ([(detalle.codigo) for detalle in obj])[0] if obj else None
        if scod == None:
            response = {'success': False, 'message': 'codigo invalido'}
            return JsonResponse(response)

        notacreditoventacab_instance = Notacreditoventacab.objects.get(pk=int(idnotacreditoventacab))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            notacreditoventadet = get_object_or_404(Notacreditoventadet, pk=idnotacreditoventadet)
            notacreditoventadet.idnotacreditoventacab =notacreditoventacab_instance
            notacreditoventadet.orden = orden
            notacreditoventadet.idarticulo = articulo_instance
            notacreditoventadet.codigo =  articulo.codigo
            notacreditoventadet.descripcion = articulo.descripcion
            notacreditoventadet.cantidad = float(cantidad)
            notacreditoventadet.unidad = articulo.unidad
            notacreditoventadet.costo =articulo.costo
            notacreditoventadet.precio = float(precio)
            notacreditoventadet.iva = articulo.iva
            notacreditoventadet.save()
            actnotacreditoventacab(idnotacreditoventacab)
            response = {'success': True}
            return JsonResponse(response)


def notacreditoventadet_eliminar(request, pk_token):
    if not request.user.has_perm('ventas.delete_notacreditoventacab'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

    idnotacreditoventadet = int(desencriptar_datos2(pk_token,request))


    notacreditoventadet_instance = Notacreditoventadet.objects.get(pk=idnotacreditoventadet)
    didnotacreditoventacab = notacreditoventadet_instance.idnotacreditoventacab_id
    print(didnotacreditoventacab)
    notacreditoventadet_instance.delete()

    orden=0
    objetos = Notacreditoventadet.objects.filter(idnotacreditoventacab=didnotacreditoventacab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actnotacreditoventacab(didnotacreditoventacab)
    response = {'success': True}
    return JsonResponse(response)



#-----------------------------------------------------------------------

@receiver(pre_save,sender=Notacreditoventadet)
def pre_save_det(sender, instance,  **kwargs):
    codigo= instance.codigo
    cantidad= instance.cantidad
    didempresa= instance.idempresa
    didsucursal= instance.idempresa
    depsalida=instance.deposito
    depentrada=instance.deposito

    try:
        previous_notadet = Notacreditoventadet.objects.get(pk=instance.pk)
    except Notacreditoventadet.DoesNotExist:
        # El objeto no existe previamente, es una creación
        previous_notadet = None
        # Ahora puedes comparar los valores anteriores con los nuevos
    if previous_notadet:
        # print("-  previous_ventadet cantidad:  " + str(instance.cantidad) + "  codigo  " + str(previous_ventadet.codigo)+"  instance.cantidad  "+str(instance.cantidad))
        # Ejemplo de comparación de campos
        if instance.cantidad != previous_notadet.cantidad:
            actualizarexistencia(codigo, instance.cantidad, previous_notadet.cantidad, depentrada, depsalida,
                                 didempresa, didsucursal)
    else:
        actualizarexistencia(codigo, instance.cantidad, 0, depentrada, '', didempresa, didsucursal)


@receiver(post_delete, sender=Notacreditoventadet)
def post_delete(sender, instance, **kwargs):
    codigo= instance.codigo
    cantidad= instance.cantidad
    didempresa= instance.idempresa
    didsucursal= instance.idempresa
    depentrada=''
    depsalida=instance.deposito
    actualizarexistencia(codigo,0,instance.cantidad,depentrada, depsalida, didempresa, didsucursal)
