from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
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




def ordencompcab_filtro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'compras/ordendecompra_filt.html')

def ordencompcab_filtro_lst(request):
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

       

    ordencompcab = Ordencompcab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)

    if idproveedor=='':
        idproveedor=0
    if ordencompcab.exists() and int(idproveedor) >=1:
            ordencompcab = ordencompcab.filter(idproveedor_id=idproveedor,idempresa=didempresa,idsucursal=didsucursal)
    if ordencompcab.exists() and  fechaini:
            fecha_inicio = datetime.strptime(fechaini, '%Y-%m-%d').date()
            ordencompcab = ordencompcab.filter(fecha__gte=fecha_inicio,idempresa=didempresa,idsucursal=didsucursal)
    if ordencompcab.exists() and  fechafin:
            fecha_fin = datetime.strptime(fechafin, '%Y-%m-%d').date()
            ordencompcab = ordencompcab.filter(fecha__lte=fecha_fin,idempresa=didempresa,idsucursal=didsucursal)
    if ordencompcab.exists() and tipodoc:
        ordencompcab = ordencompcab.filter(tipodoc=tipodoc,idempresa=didempresa,idsucursal=didsucursal)

    skey = iskey(request)

    for objeto in ordencompcab:
        objeto.pkf = encriptar_datos2(objeto.idordencompcab,request)

    cadena=""
    return render(request, 'compras/ordendecompra_lst.html', {'ordencompcab': ordencompcab, 'cadena': cadena })



def ordencompcab_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')


       

    if cadena == "*":
        ordencompcab = Ordencompcab.objects.filter(idempresa=didempresa,idsucursal=didsucursal)
        return render(request, 'compras/ordendecompra_lst.html', {'ordencompcab': ordencompcab, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'compras/ordendecompra_lst.html')

    qs = Ordencompcab.objects.filter(nombre=0,idempresa=didempresa,idsucursal=didsucursal)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):
        qs1 = Ordencompcab.objects.filter(fecha__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs1)
        qs2 = Ordencompcab.objects.filter(nrofactura__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs2)
        qs3 = Ordencompcab.objects.filter(proveedor__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union(qs3)
        qs4 = Ordencompcab.objects.filter(ruc__contains=subcadenas[i],idempresa=didempresa,idsucursal=didsucursal)
        qs = qs.union|(qs4)

    ordencompcab = qs
    return render(request, 'compras/ordendecompra_lst.html', {'ordencompcab': ordencompcab, 'cadena': cadena})

class ordencompcab_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_ordencompcab'
    model = Ordencompcab
    form_class = OrdendecompcabForm
    template_name = 'compras/ordendecompra.html'
    context_object_name = 'ordencompcab'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):
        ordencompcab = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,self.request)
            ordencompcab = Ordencompcab.objects.get(pk=pk_desencriptado)  # Recuperar la compra por su clave primaria

        context = {'ordencompcab': ordencompcab}  # Crear un diccionario de contexto
        context['title'] = ' ORDEN DE COMPRA  '
        context['sidr'] = '/ordencompcab/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['hab1']= True
        context['hab2']= False
        return render(request, self.template_name, context)

class ordencompcab_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_ordencompcab'
    #permission_required=("compras.add_ordencompcab"),("compras.change_ordencompcab")  # por ejemplo videogame_store.edit_videogame, videogame_store.delete_videogame

    model = Ordencompcab
    form_class = OrdendecompcabForm
    template_name = 'compras/ordendecompra.html'
    success_url = reverse_lazy('ordencompcab_crear')

    def dispatch(self, *args, **kwargs):
        return super(ordencompcab_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CARGAR ORDEN DE COMPRA '
        context['sidr'] = '/ordencompcab/crear/'
        context['hab1']= False
        context['hab2']= True
        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal,self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        Ordencompcab = form.save(commit=False)
        Ordencompcab.idempresa = didempresa
        Ordencompcab.idsucursal = didsucursal
        Ordencompcab.save()

        messages.success(self.request, ' orden de compra creado exitosamente.')
        response = super().form_valid(form)

        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('ordencompcab_cargar', pk_token=str(pk_encriptado))


class ordencompcab_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_ordencompcab'
    model = Ordencompcab
    form_class = OrdendecompcabForm
    template_name = 'compras/ordendecompra.html'
    success_url = '/ordencompcab/0/listar/'


    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            skey = iskey(self.request)
            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(Ordencompcab, pk=pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR COMPRAS  '
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/ordencompcab/' + pk_token + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['hab1'] = False
        context['hab2'] = True
        return context

    def get_success_url(self):
        messages.success(self.request, ' orden de compra editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('ordencompcab_cargar', kwargs={'pk_token': pk_token})

class ordencompcab_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_ordencompcab'

    def get(self, request, pk_token):

        pk = desencriptar_datos2(pk_token,request)
        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE ORDEN DE COMPRA "

        return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(Ordencompcab, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            messages.success(self.request, 'orden eliminado exitosamente.')
            return redirect('ordencompcab_cargar', pk_token=0)
        else:
            return redirect('ordencompcab_cargar', pk_token=pk_token)


def actordencompracab(idordencompcab):

    #gravada10 = Compradet.objects.filter(iva=10,idcompracab=idcompracab).aggregate(total=Sum('cantidad' * 'precio'))['total']

    detalles = Ordencompdet.objects.filter(iva=5,idordencompcab=idordencompcab)
    gravada5 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ordencompdet.objects.filter(iva=10, idordencompcab=idordencompcab)
    gravada10 = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    detalles = Ordencompdet.objects.filter(iva=0, idordencompcab=idordencompcab)
    exenta = sum([detalle.cantidad * detalle.precio for detalle in detalles])
    gravada=gravada10+gravada5
    total=gravada+exenta
    print("  idordencompcab " + str(idordencompcab))
    objetos = Ordencompcab.objects.filter(pk=idordencompcab)
    for objeto in objetos:
        objeto.gravada5 = gravada5
        objeto.gravada10 = gravada10
        objeto.gravada = gravada
        objeto.exenta = exenta
        objeto.total = total
        objeto.save()
    return total



def ordencompdet_listar(request):
    if not request.user.has_perm('compras.view_ordencompdet'):
        datos = None
        Response = JsonResponse({'datos': datos,'success': False, 'message': 'No tiene permiso para la operacion ver detalle'})
        return Response

    pk = request.POST['id_pk']
    idordencompcab = int(desencriptar_datos2(pk,request))
    orden = request.POST['orden']

    if int(orden) == 0:
        objetos = Ordencompdet.objects.filter(idordencompcab=idordencompcab).order_by('orden')
    if int(orden) >=1:
        objetos = Ordencompdet.objects.filter(idordencompcab=idordencompcab,orden=orden)
    datos = []
    for objeto in objetos:
        datos.append({
            'pkfd': encriptar_datos2(objeto.idordencompdet,request),
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


def ordencompdet_guardar(request):
    if not request.user.has_perm('compras.add_ordencompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)

    if request.method == 'POST':
        pkf = request.POST['pkf']
        pk = int(desencriptar_datos2(pkf,request))

        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        cantr = Ordencompdet.objects.filter(idordencompcab=pk).count()
        cantr=cantr+1

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        ordencompracab_instance = Ordencompcab.objects.get(pk=int(pk))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero
            ordencompdet = Ordencompdet()
            ordencompdet.idordencompcab =ordencompracab_instance
            ordencompdet.orden = cantr
            ordencompdet.idarticulo = articulo_instance
            ordencompdet.codigo =  articulo.codigo
            ordencompdet.descripcion = articulo.descripcion
            ordencompdet.cantidad = float(cantidad)
            ordencompdet.unidad = articulo.unidad
            ordencompdet.costo =articulo.costo
            ordencompdet.precio = float(precio)
            ordencompdet.iva = articulo.iva
            ordencompdet.idempresa = didempresa
            ordencompdet.idsucursal = didsucursal
            ordencompdet.save()
            actordencompracab(pk)
            response = {'success': True}
            return JsonResponse(response)

def ordencompdet_editar(request):
    if not request.user.has_perm('compras.change_ordencompdet'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)
    if request.method == 'POST':

        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pkf = request.POST['pkf']
        pk = int(desencriptar_datos2(pkf,request))
        codigo = request.POST['codigo']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        orden = request.POST['orden']
        objetos = Ordencompdet.objects.filter(idordencompcab=pk,orden=orden)
        for ordencompdet in objetos:
            idordencompdet=ordencompdet.idordencompdet

        ordencompracab_instance = Ordencompcab.objects.get(pk=int(pk))  # Asegúrate de que `idcompracab` sea un entero

        articulos = Articulo.objects.filter(codigo=float(codigo),idempresa=didempresa)
        for articulo in articulos:
            articulo_instance = Articulo.objects.get(pk=int(articulo.idarticulo))  # Asegúrate de que `idcompracab` sea un entero

            ordencompdet = get_object_or_404(Ordencompdet, pk=idordencompdet)
            ordencompdet.idcompracab =ordencompracab_instance
            ordencompdet.orden = orden
            ordencompdet.idarticulo = articulo_instance
            ordencompdet.codigo =  articulo.codigo
            ordencompdet.descripcion = articulo.descripcion
            ordencompdet.cantidad = float(cantidad)
            ordencompdet.unidad = articulo.unidad
            ordencompdet.costo =articulo.costo
            ordencompdet.precio = float(precio)
            ordencompdet.iva = articulo.iva
            ordencompdet.save()
            actordencompracab(pk)
            response = {'success': True, 'message': ''}
            return JsonResponse(response)

def ordencompdet_eliminar(request, pk_token):
    if not request.user.has_perm('compras.delete_ordencompdet'):
        response_data = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response_data)

    pk = int(desencriptar_datos2(pk_token,request))
    objetos = Ordencompdet.objects.filter(idordencompdet=pk)
    for objeto in objetos:
        idordencompcab= objeto.idordencompcab

    ordencompdet = get_object_or_404(Ordencompdet, pk=pk)
    ordencompdet.delete()

    orden=0
    objetos = Ordencompdet.objects.filter(idordencompcab=idordencompcab).order_by('orden')
    for objeto in objetos:
        objeto.orden = orden=orden+1
        objeto.save()

    actordencompracab(pk)
    response = {'success': True, 'message': ''}
    return JsonResponse(response)
