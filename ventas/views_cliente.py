from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from django.contrib import messages

def cliente_listar(request,cadena):
    idempresa = request.session.get('idempresa')
    idsucursal = request.session.get('idsucursal')
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if cadena == "*":

        cliente = Cliente.objects.filter(idempresa=didempresa)
        objetos=cliente

        for objeto in objetos:
            objeto.pkcl = encriptar_datos2(objeto.idcliente,request)

        return render(request, 'ventas/Cliente_listar.html', {'cliente': cliente, 'cadena': cadena })

    if cadena=="0":
        return render(request, 'ventas/Cliente_listar.html')

    qs = Cliente.objects.filter(nombre=0,idempresa=didempresa)
    subcadenas = cadena.split(" ")
    for i in range(len(subcadenas)):
        qs1 = Cliente.objects.filter(nombre__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs1)
        qs2 = Cliente.objects.filter(direccion__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs2)
        qs3 = Cliente.objects.filter(cedula__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs3)
        qs4 = Cliente.objects.filter(ruc__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs4)
        qs5 = Cliente.objects.filter(telefono__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs5)
        qs6 = Cliente.objects.filter(timbrado__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs6)
        qs7 = Cliente.objects.filter(direccion__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs7)
        cliente = qs
        for objeto in cliente:
            objeto.pkcl = encriptar_datos2(objeto.idcliente,request)

    return render(request, 'ventas/Cliente_listar.html', {'cliente': cliente, 'cadena': cadena})


class cliente_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'ventas.view_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/cliente.html'
    context_object_name = 'cliente'  # Nombre para acceder al objeto en la plantilla

    def get(self, request,pk_token):
        cliente = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token,request)
            cliente = Cliente.objects.get(idcliente=int(pk_desencriptado))  # Recuperar la compra por su clave primaria

        varretro = False
        if self.request.session['caja'] == 0:
            varretro = True

        context = {'cliente': cliente}  # Crear un diccionario de contexto
        context['title'] = '  CLIENTE  '
        context['sidr'] = '/cliente/' + str(pk_token) + '/cargar/'
        context['pkcl'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= True
        context['retor']= varretro
        context['pkfa']= self.request.session['pkfa']


        return render(request, self.template_name, context)


class cliente_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'ventas.add_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/cliente.html'
    success_url = reverse_lazy('cliente_crear')

    def dispatch(self, *args, **kwargs):
        return super(cliente_crear, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        varretro = False
        if self.request.session['caja'] == 1:
            varretro = True

        context = super().get_context_data(**kwargs)
        context['title'] = '  CREAR  CLIENTE '
        context['sidr'] = '/cliente/crear/'
        context['var1']= False
        context['var2']= True
        context['retor']= varretro
        context['pkfa']= self.request.session['pkfa']

        return context
    def form_valid(self, form):

        form.instance.nombre = form.cleaned_data['nombre'].upper()
        form.instance.cedula = form.cleaned_data['cedula'].upper()
        form.instance.direccion = form.cleaned_data['direccion'].upper()
        form.instance.ciudad = form.cleaned_data['ciudad'].upper()

        idempresa = self.request.session.get('idempresa')
        idsucursal = self.request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        Cliente = form.save(commit=False)
        Cliente.idempresa = didempresa
        Cliente.idsucursal = didsucursal
        Cliente.save()

        response = super().form_valid(form)
        messages.success(self.request, 'Cliente creado exitosamente.')
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('cliente_cargar', pk_token=str(pk_encriptado))


class cliente_editar(LoginRequiredMixin,ValidarPermisoMixin,UpdateView):
    permission_required = 'ventas.change_cliente'
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/cliente.html'
    success_url = '/cliente/0/listar/'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        print(pk_token)

        if pk_token != "0":
            pk = desencriptar_datos2(pk_token,self.request)
            return get_object_or_404(Cliente, pk=pk)

    def get_context_data(self, **kwargs):
        varretro = False
        if self.request.session['caja'] == 1:
            varretro = True

        pk_token = self.kwargs['pk_token']
        context = super().get_context_data(**kwargs)
        context['title'] = '  EDITAR  CLIENTE '
        context['sidr'] = '/cliente/'+ str(pk_token) + '/editar/'
        context['pkcl'] = pk_token
        context['var1']= False
        context['var2']= True
        context['retor']= varretro
        context['pkfa']= self.request.session['pkfa']

        return context

    def form_valid(self, form):
        form.instance.nombre = form.cleaned_data['nombre'].upper()
        form.instance.cedula = form.cleaned_data['cedula'].upper()
        form.instance.direccion = form.cleaned_data['direccion'].upper()
        form.instance.ciudad = form.cleaned_data['ciudad'].upper()

        pk_token = self.kwargs['pk_token']
        response = super().form_valid(form)

        messages.success(self.request, 'cliente editado exitosamente.')
        return redirect('cliente_cargar', pk_token=str(pk_token))


class cliente_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'ventas.delete_cliente'

    def get(self, request, pk_token):
        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO DE ClIENTE "
        if pk_token == "0":
            return redirect('cliente_cargar', pk_token=0)
        else:
            return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        print(" CLIENTE PARA ELIMINAR " + action)

        if action == 'CONFIRMAR':
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(Cliente, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            return redirect('cliente_cargar', pk_token=0)
        else:
            return redirect('cliente_cargar', pk_token=pk_token)


def cli_datos(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        # Obtenemos una lista de instancias de modelo
        #objetos = Cliente.objects.all()
        objetos = Cliente.objects.filter(idcliente=pk)
        # Convertimos cada instancia de modelo a un diccionario y los agregamos a una lista
        datos = []
        for objeto in objetos:
            datos.append({
                'idcliente': objeto.idcliente,
                'cliente': objeto.nombre,
                'ruc': objeto.ruc,
                'timbrado': objeto.timbrado,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response


def cli_ci_ruc(request):
    if request.method == 'POST':
        valor = request.POST['valor']

        # Obtenemos una lista de instancias de modelo
        #objetos = Cliente.objects.all()
        objetos = Cliente.objects.filter(cedula=valor)
        cantr = objetos.count()
        if cantr == 0:
            objetos = Cliente.objects.filter(ruc=valor)

        # Convertimos cada instancia de modelo a un diccionario y los agregamos a una lista
        datos = []
        for objeto in objetos:
            datos.append({
                'idcliente': objeto.idcliente,
                'cliente': objeto.nombre,
                'ruc': objeto.ruc,
                'cedula': objeto.cedula,
                'timbrado': objeto.timbrado,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response

def cmbcli(request):
    if request.method == 'POST':
        idempresa = request.session.get('idempresa')
        idsucursal = request.session.get('idsucursal')
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)

        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        objetos = Cliente.objects.filter(idempresa=didempresa)
        datos = []
        for objeto in objetos:
            datos.append({
                'idcliente': objeto.idcliente,
                'cliente': objeto.nombre,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response
