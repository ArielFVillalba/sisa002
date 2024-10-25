from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from sisa.mixins import ValidarPermisoMixin


# Create your views here.
class UsuarioListado(LoginRequiredMixin, ValidarPermisoMixin, ListView):
    permission_required = 'usuario.view_usuario'
    model = usuario
    template_name = 'usuario/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in usuario.objects.all():
                    if i is None:
                        print("Es none")
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuario'
        context['create_url'] = reverse_lazy('usuario:Usuarios_crear')
        context['list_url'] = reverse_lazy('usuario:Usuarios_listado')
        context['entity'] = 'Usuarios'
        return context

# class Usuario_crear(LoginRequiredMixin, ValidarPermisoMixin, CreateView):
#     model = usuario
#     form_class = usuarioForm
#     template_name = 'usuario/crear.html'
#     success_url = reverse_lazy('usuario:Usuarios_listado')
#     permission_required = 'usuario.add_usuario'
#     url_redirect = success_url
#
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'add':
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Creación de un Usuario'
#         context['entity'] = 'Usuarios'
#         context['list_url'] = self.success_url
#         context['action'] = 'add'
#         return context
class Usuario_crear(LoginRequiredMixin, ValidarPermisoMixin, CreateView):
    model = usuario
    form_class = usuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('usuario:Usuarios_listado')
    permission_required = 'usuario.add_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class UsuarioEditar(ValidarPermisoMixin, UpdateView):
    model = usuario
    form_class = usuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('usuario:Usuarios_listado')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        context['create_url2'] = reverse_lazy('usuario:Usuarios_listado')
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
class UsuarioBorrar(ValidarPermisoMixin, DeleteView):
    model = usuario
    template_name = 'usuario/borrar.html'
    success_url = reverse_lazy('usuario:Usuarios_listado')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        # context['action'] = 'delete'
        return context
