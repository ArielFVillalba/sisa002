from django.contrib.admin.models import CHANGE
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum


def proveedor_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if cadena == "*":
        proveedor = Proveedor.objects.filter(idempresa=didempresa)
        objetos = proveedor

        for objeto in objetos:
            objeto.pkpr = encriptar_datos2(objeto.idproveedor,request)

        return render(request, 'compras/proveedor_listar.html', {'proveedor': proveedor, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'compras/proveedor_listar.html')


    subcadenas = cadena.split(" ")
    qs = Proveedor.objects.filter(nombre="0")
    for i in range(len(subcadenas)):
        qs1 = Proveedor.objects.filter(nombre__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs1)
        qs2 = Proveedor.objects.filter(direccion__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs2)
        qs3 = Proveedor.objects.filter(cedula__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs3)
        qs4 = Proveedor.objects.filter(ruc__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs4)
        qs5 = Proveedor.objects.filter(telefono__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs5)
        qs6 = Proveedor.objects.filter(timbrado__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs6)
        qs7 = Proveedor.objects.filter(direccion__contains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs7)
       
        proveedor = qs
        objetos = proveedor
        skey = iskey(request)
        for objeto in objetos:
            objeto.pkpr = encriptar_datos2(objeto.idproveedor,request)
            objeto.save()

    return render(request, 'compras/proveedor_listar.html', {'proveedor': proveedor, 'cadena': cadena})

class proveedor_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'compras.view_proveedor'
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'compras/proveedor.html'
    context_object_name = 'proveedor'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):

        proveedor = None
        if pk_token != "0":
            skey=iskey(request)
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            proveedor = Proveedor.objects.get(idproveedor=int(pk_desencriptado))  # Recuperar la compra por su clave primaria

        context = {'proveedor': proveedor}  # Crear un diccionario de contexto
        context['title'] = '  PROVEEDOR  '
        context['sidr'] = '/proveedor/' + str(pk_token) + '/cargar/'
        context['pkpr'] = pk_token
        context['var1']= True
        context['var2']= False

        return render(request, self.template_name, context)


class proveedor_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'compras.add_proveedor'
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'compras/proveedor.html'
    success_url = reverse_lazy('proveedor_crear')

    def dispatch(self, *args, **kwargs):

        return super(proveedor_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  CREAR  PROVEEDOR '
        context['sidr'] = '/proveedor/crear/'
        context['var1']= False
        context['var2']= True

        return context

    def form_valid(self, form):
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        proveedor = form.save(commit=False)
        proveedor.idempresa = didempresa
        proveedor.idsucursal = didsucursal
        proveedor.save()

        response = super().form_valid(form)
        messages.success(self.request, 'proveedor creado exitosamente.')
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente

        return redirect('proveedor_cargar', pk_token=str(pk_encriptado))


class proveedor_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'compras.change_proveedor'
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'compras/proveedor.html'
    success_url = '/proveedor/0/listar/'


    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,self.request)
            user = self.request.user
            return get_object_or_404(Proveedor, pk=pk)


    def get_context_data(self, **kwargs):
        pk_token = self.kwargs['pk_token']
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR  PROVEEDOR '
        context['sidr'] = '/proveedor/'+ str(pk_token) + '/editar/'
        context['pkpr'] = pk_token
        context['var1']= False
        context['var2']= True
        return context

    def form_valid(self, form):
        pk_token = self.kwargs['pk_token']
        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        response = super().form_valid(form)
        messages.success(self.request, 'proveedor editado exitosamente.')
        return redirect('proveedor_cargar', pk_token=str(pk_token))


def proveedor2_eliminar(request, pk_token):
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    pk = desencriptar_datos2(pk_token,request)
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    response = {'success': True}
    return JsonResponse(response)

class proveedor_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'compras.delete_proveedor'

    def get(self, request, pk_token):
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        titulo="¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg=" EL REGISTRO DE PROVEEDOR "
        if pk_token == "0":
            return redirect('proveedor_cargar', pk_token=0)
        else:
            return render(request, 'base/pagcofirmacion.html', {'instance': msg,'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':
            skey = iskey(request)
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(Proveedor, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            return redirect('proveedor_cargar', pk_token=0)
        else:
            return redirect('proveedor_cargar', pk_token=pk_token)


def prov_datos(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        # Obtenemos una lista de instancias de modelo
        #objetos = Proveedor.objects.all()
        objetos = Proveedor.objects.filter(idproveedor=pk)
        # Convertimos cada instancia de modelo a un diccionario y los agregamos a una lista
        datos = []
        for objeto in objetos:
            datos.append({
                'idproveedor': objeto.idproveedor,
                'nombre': objeto.nombre,
                'ruc': objeto.ruc,
                'timbrado': objeto.timbrado,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response


def cmbprov2(request):
    if request.method == 'POST':
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        proveedor = Proveedor.objects.filter(idempresa=didempresa).values_list('nombre', flat=True)
        nombres = list(proveedor)
        Response = JsonResponse({'datos': nombres})
        return Response

def cmbprov(request):
    if request.method == 'POST':
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        objetos = Proveedor.objects.filter(idempresa=didempresa)
        datos = []
        for objeto in objetos:
            datos.append({
                'idproveedor': objeto.idproveedor,
                'nombre': objeto.nombre,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response

