import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect , get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from compras.models import Compracab, Compradet
from sisa import settings
from sisa.mixins import ValidarPermisoMixin
from inicio.funcion import *
from .forms import *
from django.contrib import messages
from django.core.serializers import json
from django.db.models import Sum, F
from django.db.models import Func

def articulos_listar(request,cadena):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    #stockdet()
    if cadena == "*"  or cadena == "0" or cadena == "":
        articulos = Articulo.objects.filter(idempresa=didempresa)
        for objeto in articulos:
            objeto.pka = encriptar_datos2(objeto.idarticulo, request)
        articulos = recargararticulo(articulos, didempresa)
        return render(request, 'stock/articulos_listar.html', {'articulos': articulos, 'cadena': ""})

    #if cadena == "0":
    #    return render(request, 'stock/articulos_listar.html')

    articulos = Articulo.objects.filter(idempresa=didempresa)
    qs = articulos.filter(codigo=0)
    subcadenas = cadena.split(" ")

    for subcadena in subcadenas:
        if subcadena != "":
            qs1 = articulos.filter(codigo__icontains=subcadena)
            qs = qs.union(qs1)
            qs2 = articulos.filter(descripcion__icontains=subcadena)
            qs = qs.union(qs2)
            # qs3 = articulos.filter(unidad__icontains=subcadena)
            # qs = articulos.union(qs3)
            # qs4 = articulos.filter(costo__icontains=subcadena)
            # qs = qs.union(qs4)
            # qs5 = articulos.filter(precio__icontains=subcadena)
            # qs = qs.union(qs5)
            # qs6 = articulos.filter(iva__icontains=subcadena)
            # qs = qs.union(qs6)
            scodflia = filtrarfliacod(didempresa, 'familia1', 'n1', subcadena)
            if scodflia != '':
                qs7 = articulos.filter(codigoflia__icontains=scodflia)
                qs = qs.union(qs7)
            scodflia = filtrarfliacod(didempresa, 'familia2', 'n2', subcadena)
            if scodflia != '':
                qs8 = articulos.filter(codigoflia__icontains=scodflia)
                qs = qs.union(qs8)
            scodflia = filtrarfliacod(didempresa, 'familia3', 'n3', subcadena)
            if scodflia != '':
                qs9 = articulos.filter(codigoflia__icontains=scodflia)
                qs = qs.union(qs9)
            scodflia = filtrarfliacod(didempresa, 'familia4', 'n4', subcadena)
            if scodflia != '':
                qs10 = articulos.filter(codigoflia__icontains=scodflia)
                qs = qs.union(qs10)
            scodflia = filtrarfliacod(didempresa, 'familia5', 'n5', subcadena)
            if scodflia != '':
                qs11 = articulos.filter(codigoflia__icontains=scodflia)
                qs = qs.union(qs11)
            scodflia = filtrarfliacod(didempresa, 'familia6', 'n6', subcadena)
            if scodflia != '':
                qs12 = articulos.filter(codigoflia__icontains=scodflia)
                qs = qs.union(qs12)
            scodflia = filtrarfliacod(didempresa, 'familia7', 'n7', subcadena)
            if scodflia != '':
                qs13 = articulos.filter(codigoflia__icontains=scodflia)
                qs = qs.union(qs13)

            auxarticulos = qs
            for objeto in auxarticulos:
                objeto.pka = encriptar_datos2(objeto.idarticulo,request )
            auxarticulos = recargararticulo(auxarticulos, didempresa)

    return render(request, 'stock/articulos_listar.html', {'articulos': auxarticulos, 'cadena': cadena})


def mostarcodflia(codigo):
    print(' mostarcodflia ' + str(codigo))
    if codigo == 'None':
        return ''

    val = ''
    x = codigo.split('.')
    for y in x:
        if int(y) > 0:
            if val != '':
                val = val + '.'
            val = val + y
    return val


def recargararticulo(articulo, didempresa):
    for objeto in articulo:
        objeto.familia1 = ''
        objeto.familia2 = ''
        objeto.familia3 = ''
        objeto.familia4 = ''
        objeto.familia5 = ''
        objeto.familia6 = ''
        objeto.familia7 = ''
        if objeto.codigoflia is not None and objeto.codigoflia:
            cod = mostarcodflia(objeto.codigoflia)
            qs = familia.objects.filter(codigo=cod, idempresa=didempresa)
            for ob in qs:
                # print(' os qo' + str(ob.familia1))
                objeto.familia1 = ob.familia1
                objeto.familia2 = ob.familia2
                objeto.familia3 = ob.familia3
                objeto.familia4 = ob.familia4
                objeto.familia5 = ob.familia5
                objeto.familia6 = ob.familia6
                objeto.familia7 = ob.familia7

    return articulo


def recargararticuloget(articulo, didempresa):
    articulo.familia1 = ''
    articulo.familia2 = ''
    articulo.familia3 = ''
    articulo.familia4 = ''
    articulo.familia5 = ''
    articulo.familia6 = ''
    articulo.familia7 = ''
    if articulo.codigoflia is not None and articulo.codigoflia:
        cod = mostarcodflia(articulo.codigoflia)
        qs = familia.objects.filter(codigo=cod, idempresa=didempresa)
        for ob in qs:
            # print(' os qo' + str(ob.familia1))
            articulo.familia1 = ob.familia1
            articulo.familia2 = ob.familia2
            articulo.familia3 = ob.familia3
            articulo.familia4 = ob.familia4
            articulo.familia5 = ob.familia5
            articulo.familia6 = ob.familia6
            articulo.familia7 = ob.familia7
    return articulo


def filtrarfliacod(didempresa, auxfamilia, n, valorcod):
    filtro = {f"{auxfamilia}__icontains": valorcod, "idempresa": didempresa}
    obj = familia.objects.filter(**filtro)
    cod = getattr(obj.first(), n) if obj.exists() else ''
    print(str(cod))
    return cod


class articulos_cargar(LoginRequiredMixin,ValidarPermisoMixin,View):
    permission_required = 'stock.view_articulo'

    model = Articulo
    form_class = ArticuloForm
    template_name = 'stock/articulo.html'
    success_url = reverse_lazy('articulos_crear')

    def get(self, request,pk_token):
        articulo = None
        if pk_token != "0":
            idempresa = request.session['idempresa']
            idsucursal = request.session['idsucursal']
            didempresa = desencriptar_datos2(idempresa, request)
            didsucursal = desencriptar_datos2(idsucursal, request)
            if int(didempresa) < 1 or int(didsucursal) < 1:
                return redirect('login')

            pk_desencriptado = desencriptar_datos2(pk_token, request)
            articulo = Articulo.objects.get(idarticulo=int(pk_desencriptado))  # Recuperar la compra por su clave primaria
            articulo = recargararticuloget(articulo, didempresa)

        context = {'articulo': articulo}  # Crear un diccionario de contexto
        context['title'] = '  ARTICULO  '
        context['sidr'] = '/articulos/' + str(pk_token) + '/cargar/'
        context['pka'] = pk_token
        context['pk_token'] = pk_token
        context['var1']= True
        context['var2']= False

        return render(request, self.template_name, context)



class articulos_crear(LoginRequiredMixin,ValidarPermisoMixin,CreateView):
    permission_required = 'stock.add_articulo'
    model = Articulo
    form_class = ArticuloForm
    template_name = 'stock/articulo.html'
    success_url = reverse_lazy('articulos_crear')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '  CREAR  ARTICULO '
        context['sidr'] = '/articulos/crear/'
        context['var1']= False
        context['var2']= True
        return context

    def form_valid(self, form):
        # Convertir campos a mayúsculas antes de guardar
        form.instance.descripcion = form.cleaned_data['descripcion'].upper()
        form.instance.unidad = form.cleaned_data['unidad'].upper()
        idempresa = self.request.session['idempresa']
        idsucursal = self.request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        if Articulo.objects.filter(codigo=form.cleaned_data['codigo'], idempresa=didempresa).exists():
            messages.success(self.request, 'el codigo ya existe.')
            return redirect('articulos_cargar', pk_token=0)

        articulo = form.save(commit=False)
        articulo.idempresa = didempresa
        articulo.idsucursal = didsucursal
        articulo.save()

        response = super().form_valid(form)
        messages.success(self.request, 'Artículo agregado exitosamente.')
        skey = iskey(self.request)
        pk_encriptado = encriptar_datos2(self.object.pk,self.request)  # Asegúrate de que esta función esté implementada correctamente
        return redirect('articulos_cargar', pk_token=str(pk_encriptado))


class articulos_editar(LoginRequiredMixin, ValidarPermisoMixin, UpdateView):
    permission_required = 'stock.chance_articulo'
    model = Articulo
    form_class = ArticuloForm
    template_name = 'stock/articulo.html'

    def get_object(self,queryset=None):
        pk_token = self.kwargs['pk_token']
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            return get_object_or_404(Articulo, pk=pk)

    def get_context_data(self, **kwargs):
        skey = iskey(self.request)
        idempresa = self.request.session['idempresa']
        idsucursal = self.request.session['idsucursal']
        didempresa = desencriptar_datos2(idempresa, self.request)
        didsucursal = desencriptar_datos2(idsucursal, self.request)
        if int(didempresa) < 1 or int(didsucursal) < 1:
            return redirect('login')

        pk_token = self.kwargs['pk_token']
        articulos=None
        if pk_token != "0":
            pk = desencriptar_datos2(pk_token, self.request)
            articulos = Articulo.objects.get(idarticulo=int(pk))
            articulos = recargararticuloget(articulos, didempresa)

        context = super().get_context_data(**kwargs)
        context['articulo'] = articulos  # Crear un diccionario de contexto
        context['title'] = 'EDITAR  ARTICULO'
        pk_token = self.kwargs['pk_token']
        context['sidr'] = '/articulos/' + str(pk_token) + '/editar/'
        context['pk_token'] = pk_token
        context['pka'] = pk_token
        context['var1'] = False
        context['var2'] = True
        return context

    def form_valid(self, form):
        # Convertir campos a mayúsculas antes de guardar
        form.instance.descripcion = form.cleaned_data['descripcion'].upper()
        form.instance.unidad = form.cleaned_data['unidad'].upper()

        if form.cleaned_data['habilitado']:
            print("--------" + str(form.cleaned_data['habilitado']))
        else:
            print(" ------ no true " + str(form.cleaned_data['habilitado']))

            # Realiza alguna acción si 'habilitado' es False
            pass

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'articulo editado exitosamente.')
        pk_token = self.kwargs['pk_token']
        return reverse_lazy('articulos_cargar', kwargs={'pk_token': pk_token})




class articulos_eliminar(LoginRequiredMixin,ValidarPermisoMixin, View):
    permission_required = 'stock.delete_articulo'

    def get(self, request, pk_token):
        titulo = "¿ESTA SEGURO QUE DESEA ELIMINAR? "
        msg = " EL REGISTRO  "
        if pk_token == "0":
            return redirect('articulos_cargar', pk_token=0)
        else:
            return render(request, 'base/pagcofirmacion.html', {'instance': msg, 'titulo': titulo})

    def post(self, request, pk_token):
        action = request.POST.get('action')
        print(" CLIENTE PARA ELIMINAR " + action)

        if action == 'CONFIRMAR':

            pk = desencriptar_datos2(pk_token,request)
            instance = get_object_or_404(Articulo, pk=pk)
            try:
                instance.delete()
            except Exception as e:
                return render(request, 'error_page.html', {'error_message': str(e)})
            return redirect('articulos_cargar', pk_token=0)
        else:
            return redirect('articulos_cargar', pk_token=pk_token)



def cmbarticulo(request):
    if not request.user.is_authenticated:
        return redirect('login')
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)

    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')
    
    if request.method == 'POST':
        objetos = Articulo.objects.filter(idempresa=didempresa)
        datos = []
        for objeto in objetos:
            datos.append({
                'codigo': objeto.codigo,
                'descripcion': objeto.descripcion,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response

def articulodatos(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        codigo = request.POST['codigo']
        datos=None
        if len(codigo) >2:
            objetos = Articulo.objects.filter(codigo=codigo,idempresa=didempresa)
            datos = []
            for objeto in objetos:
                datos.append({
                    'descripcion': objeto.descripcion,
                    'precio': objeto.precio,
                    'iva': objeto.iva,
            })

        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response


def articulodatosdesc(request):
    if not request.user.is_authenticated:
        return redirect('login')

    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST':
        desc = request.POST['desc']
        datos=None
        if len(desc) >2:
            objetos = Articulo.objects.filter(descripcion__iexact=desc,idempresa=didempresa)
            datos = []
            for objeto in objetos:
                datos.append({
                    'codigo': objeto.codigo,
                    'descripcion': objeto.descripcion,
                    'precio': objeto.precio,
                    'iva': objeto.iva,
            })
        # Creamos una respuesta JSON utilizando la lista de diccionarios convertidos
        Response = JsonResponse({'datos': datos})
        return Response

def stockdet(fechaini,fechafin,codigo,deposito,sucursal):

    sql= "select *  from fc_lstexistdetalle( '"+ fechaini +"', '"+ fechafin +"','"+ codigo +"','"+ deposito +"','"+ sucursal +"');"
    #sql="select  *  from listadoview"
    valor1 = seleccionar_datos3( sql)
    print(valor1)
    return valor1

def articulosubirimagen(request):
    idempresa = request.session['idempresa']
    idsucursal = request.session['idsucursal']
    didempresa = desencriptar_datos2(idempresa, request)
    didsucursal = desencriptar_datos2(idsucursal, request)
    if int(didempresa) < 1 or int(didsucursal) < 1:
        return redirect('login')

    if request.method == 'POST' and request.FILES.get('imagen'):
        codigo = request.POST['codigo']
        print(str(codigo))

        imagen = request.FILES['imagen']  # Obtiene el archivo de la solicitud
        # Aquí puedes procesar la imagen como desees, por ejemplo, guardarla en disco
        # Asegúrate de validar la extensión, el tamaño y realizar otras medidas de seguridad
        # Verificar si la carpeta existe, si no existe, crearla
        carpeta_destino = os.path.join(settings.STATICFILES_DIRS[0], 'imagen/articulos/'+str(didempresa)+'/')
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        # Ruta de destino dentro de la carpeta 'imagenes'
        ruta_destino = os.path.join(carpeta_destino)

        # Ejemplo de guardado de la imagen en disco
        #ruta_destino = os.path.join(settings.STATICFILES_DIRS[0], 'imagen/articulos/', imagen.name)
        #ruta_destino = os.path.join(settings.STATICFILES_DIRS[0], 'imagen/articulos/')

        with open(ruta_destino + imagen.name, 'wb+') as destino:
            for chunk in imagen.chunks():
                destino.write(chunk)

        return JsonResponse({'mensaje': 'Imagen subida exitosamente.'})
    else:
        return JsonResponse({'error': 'No se proporcionó ningún archivo o el método de solicitud no es POST.'})


