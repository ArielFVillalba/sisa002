from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from compras.models import Compracab, Compradet
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum, F
from django.db.models import Func

def familia_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    #stockdet()
    cant=len(cadena)

    if cadena == "*"  or cadena == "0" or cadena == "":

        ifamilia = familia.objects.filter(idempresa=didempresa).order_by('n1','n2','n3','n4','n5','n6','n7')
        for objeto in ifamilia:
            objeto.pkf = encriptar_datos2(objeto.idfamilia,request)
        return render(request, 'stock/familia_listar.html', {'familia': ifamilia, 'cadena': '' })

    if cant<2:
        ifamilia = familia.objects.filter(idempresa=didempresa).order_by('n1','n2','n3','n4','n5','n6','n7')
        for objeto in ifamilia:
            objeto.pkf = encriptar_datos2(objeto.idfamilia,request)
        return render(request, 'stock/familia_listar.html', {'familia': ifamilia, 'cadena': cadena })


    qs = familia.objects.filter(codigo=0,idempresa=didempresa)
    subcadenas = cadena.split(" ")

    for i in range(len(subcadenas)):

        qs1 = familia.objects.filter(codigo__icontains=subcadenas[i],idempresa=didempresa)
        qs=qs.union(qs1)
        qs7 = familia.objects.filter(familia1__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs7)
        qs8 = familia.objects.filter(familia2__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs8)
        qs9 = familia.objects.filter(familia3__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs9)
        qs10 = familia.objects.filter(familia4__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs10)
        qs11 = familia.objects.filter(familia5__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs11)
        qs12 = familia.objects.filter(familia6__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs12)
        qs13 = familia.objects.filter(familia7__icontains=subcadenas[i],idempresa=didempresa)
        qs = qs.union(qs13)
        ifamilia = qs.order_by('n1','n2','n3','n4','n5','n6','n7')

        for objeto in ifamilia:
            objeto.pkf = encriptar_datos2(objeto.idfamilia,request)

    return render(request, 'stock/familia_listar.html', {'familia': ifamilia ,'cadena': cadena})


class familia_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'stock.view_familia'
    model = familia
    form_class = FamiliaForm
    template_name = 'stock/familia.html'
    success_url = reverse_lazy('familia_crear')

    def get(self, request,pk_token):
        ifamilia = None
        if pk_token != "0":
            pk_desencriptado = desencriptar_datos2(pk_token, request)
            ifamilia = familia.objects.get(idfamilia=int(pk_desencriptado))  # Recuperar la compra por su clave primaria

        context = {'familia': ifamilia}  # Crear un diccionario de contexto
        context['title'] = '  FAMILIA  '
        context['sidr'] = '/familia/' + str(pk_token) + '/cargar/'
        context['pkf'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= True
        context['var2']= False

        return render(request, self.template_name, context)


class familia_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'stock.add_familia'
    model = familia
    form_class = FamiliaForm
    template_name = 'stock/familia.html'
    success_url = reverse_lazy('familia_crear')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  CREAR FAMILIA '
        context['sidr'] = '/familia/crear/'
        context['var1']= False
        context['var2']= True

        return context

    def form_valid(self, form):
        # Convertir campos a mayúsculas antes de guardar

        form.instance.familia1 = form.cleaned_data['familia1'].upper()
        form.instance.familia2 = form.cleaned_data['familia2'].upper()
        form.instance.familia3 = form.cleaned_data['familia3'].upper()
        form.instance.familia4 = form.cleaned_data['familia4'].upper()
        form.instance.familia5 = form.cleaned_data['familia5'].upper()
        form.instance.familia6 = form.cleaned_data['familia6'].upper()
        form.instance.familia7 = form.cleaned_data['familia7'].upper()
        codigo = form.cleaned_data['codigo']
        idempresa = self.request.session['idempresa']
        idsucursal = self.request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)

        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        familia = form.save(commit=False)
        familia.idempresa = didempresa
        familia.idsucursal = didsucursal
        familia.save()

        response = super().form_valid(form)
        actualizarfamilia(codigo,self.object.pk)

        messages.success(self.request, 'Familia agregado exitosamente.')
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('familia_cargar', pk_token=str(pk_encriptado))



class familia_editar(LoginRequiredMixin, ValidarPermisoMixin, UpdateView):
    permission_required = 'stock.chance_familia'
    model = familia
    form_class = FamiliaForm
    template_name = 'stock/familia.html'

    def get_object(self, queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            return get_object_or_404(familia, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EDITAR FAMILIA'
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/familia/' + str(pk_token) + '/editar/'
        context['pk_token'] = pk_token
        context['pkf'] = pk_token
        context['var1'] = False
        context['var2'] = True
        return context

    def form_valid(self, form):
        # Convertir campos a mayúsculas antes de guardar

        form.instance.familia1 = form.cleaned_data['familia1'].upper()
        form.instance.familia2 = form.cleaned_data['familia2'].upper()
        form.instance.familia3 = form.cleaned_data['familia3'].upper()
        form.instance.familia4 = form.cleaned_data['familia4'].upper()
        form.instance.familia5 = form.cleaned_data['familia5'].upper()
        form.instance.familia6 = form.cleaned_data['familia6'].upper()
        form.instance.familia7 = form.cleaned_data['familia7'].upper()

        return super().form_valid(form)

    def get_success_url(self):
        actualizarfamilia(self.object.codigo,self.object.pk)

        messages.success(self.request, 'familia editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('familia_cargar', kwargs={'pk_token': pk_token})


class familia_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'stock.delete_familia'

    def get(self, request, pk_token):
        idempresa = request.session['idempresa']
        idsucursal = request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, request)
        didsucursal = desencriptar_datos2(idsucursal, request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO  "
        if pk_token == "0":
            return redirect('familia_cargar', pk_token=0)
        else:
            return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')

        if action == 'CONFIRMAR':

            skey = iskey(request)
            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(familia, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            return redirect('familia_cargar', pk_token=0)
        else:
            return redirect('familia_cargar', pk_token=pk_token)


def actualizarfamilia(codigo,idfamilia):
    n1=0;  n2=0; n3=0; n4=0; n5=0; n6=0; n7=0;
    icod=codigo.split(".")
    nivel=len(icod)

    if nivel >= 1:
        n1=icod[0]
    if nivel >= 2:
        n2=icod[1]
    if nivel >= 3:
        n3=icod[2]
    if nivel >= 4:
        n4=icod[3]
    if nivel >= 5:
        n5=icod[4]
    if nivel >= 6:
        n6=icod[5]
    if nivel >= 7:
        n7=icod[6]

    objetos = familia.objects.filter(idfamilia=idfamilia)
    for objeto in objetos:
        objeto.n1 = n1
        objeto.n2 = n2
        objeto.n3 = n3
        objeto.n4 = n4
        objeto.n5 = n5
        objeto.n6 = n6
        objeto.n7 = n7
        objeto.save()


def cmbfamilia(request):
    if not request.user.has_perm('stock.view_familia'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        codigo = request.POST['codigo']
        n1 = 0;
        n2 = 0;
        n3 = 0;
        n4 = 0;
        n5 = 0;
        n6 = 0;
        n7 = 0;
        icod = codigo.split(".")
        nivel = len(icod)

        if nivel >= 1:
            n1 = icod[0]
        if nivel >= 2:
            n2 = icod[1]
        if nivel >= 3:
            n3 = icod[2]
        if nivel >= 4:
            n4 = icod[3]
        if nivel >= 5:
            n5 = icod[4]
        if nivel >= 6:
            n6 = icod[5]
        if nivel >= 7:
            n7 = icod[6]

        if codigo=="0":
            nivel = 1
        else:
            nivel =nivel+1
        if nivel == 1:
            objetos = familia.objects.filter(idempresa=didempresa,n2=0,n3=0,n4=0,n5=0,n6=0,n7=0)
        if nivel == 2:
            objetos = familia.objects.filter(idempresa=didempresa,n1=n1,n3=0,n4=0,n5=0,n6=0,n7=0)
        if nivel == 3:
            objetos = familia.objects.filter(idempresa=didempresa,n1=n1,n2=n2,n4=0,n5=0,n6=0,n7=0)
        if nivel == 4:
            objetos = familia.objects.filter(idempresa=didempresa,n1=n1,n2=n2,n3=n3,n5=0,n6=0,n7=0)
        if nivel == 5:
            objetos = familia.objects.filter(idempresa=didempresa, n1=n1,n2=n2,n3=n3,n4=n4,n6=0, n7=0)
        if nivel == 6:
            objetos = familia.objects.filter(idempresa=didempresa,n1=n1,n2=n2,n3=n3,n4=n4,n5=n5, n7=0)
        if nivel == 7:
            objetos = familia.objects.filter(idempresa=didempresa,n1=n1,n2=n2,n3=n3,n4=n4,n5=n5, n6=n6)

        datos = []
        for objeto in objetos:

                if nivel == 1:
                    datos.append({'familia': objeto.familia1,'codigo': objeto.codigo,})
                if nivel == 2:
                    datos.append({'familia': objeto.familia2,'codigo': objeto.codigo,})
                if nivel == 3:
                    datos.append({'familia': objeto.familia3,'codigo': objeto.codigo,})
                if nivel == 4:
                    datos.append({'familia': objeto.familia4,'codigo': objeto.codigo,})
                if nivel == 5:
                    datos.append({'familia': objeto.familia5,'codigo': objeto.codigo,})
                if nivel == 6:
                    datos.append({'familia': objeto.familia6,'codigo': objeto.codigo,})
                if nivel == 7:
                    datos.append({'familia': objeto.familia7,'codigo': objeto.codigo,})

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response


def familia_buscar(request):
    if not request.user.has_perm('stock.view_familia'):
        response = {'success': False, 'message': 'No tiene permiso para esta operacion'}
        return JsonResponse(response)
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)

    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        codigo = request.POST['codigo']

        if codigo=="0":
            qs = familia.objects.filter(idempresa=didempresa)
            objetos = qs.order_by('n1','n2','n3','n4','n5','n6','n7')

        if len(codigo)>1:
            n1 = 0;
            n2 = 0;
            n3 = 0;
            n4 = 0;
            n5 = 0;
            n6 = 0;
            n7 = 0;
            icod = codigo.split("_")
            nivel = len(icod)

            if nivel >= 1:
                n1 = icod[0]
            if nivel >= 2:
                n2 = icod[1]
            if nivel >= 3:
                n3 = icod[2]
            if nivel >= 4:
                n4 = icod[3]
            if nivel >= 5:
                n5 = icod[4]
            if nivel >= 6:
                n6 = icod[5]
            if nivel >= 7:
                n7 = icod[6]

            codigo = codigo.replace('_', '.')  # Reemplazar 'o' por 'a'

            qs = familia.objects.filter(codigo=codigo,idempresa=didempresa)
            objetos = qs.order_by('n1','n2','n3','n4','n5','n6','n7')

        datos = []
        for objeto in objetos:
            datos.append({
                'codigo': objeto.codigo,
                'n1': objeto.n1,
                'n2': objeto.n2,
                'n3': objeto.n3,
                'n4': objeto.n4,
                'n5': objeto.n5,
                'n6': objeto.n6,
                'n7': objeto.n7,
                'familia1': objeto.familia1,
                'familia2': objeto.familia2,
                'familia3': objeto.familia3,
                'familia4': objeto.familia4,
                'familia5': objeto.familia5,
                'familia6': objeto.familia6,
                'familia7': objeto.familia7,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response
