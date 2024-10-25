from datetime import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_str

class IsSuperMixins(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('/menu')

    def dispatch(self, request, *args, **kwargs):
        if not self.tiene_permiso(request):
            # Redireccionar al módulo anterior (página de referencia)
            return redirect(request.META.get('HTTP_REFERER'))
        return super().dispatch(request, *args, **kwargs)

class ValidarPermisoMixinori(SuccessMessageMixin):
    permission_required = ''
    url_redirect = None
    permission_denied_message = "You do not have permission to access this page."

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            if self.url_redirect:
                return HttpResponseRedirect(self.url_redirect)
            else:
                messages.error(request, 'No tiene permiso para ingresar a este módulo')
                return redirect(request.META.get('HTTP_REFERER'))

        return super().dispatch(request, *args, **kwargs)


class ValidarPermisoMixinandajina(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('login')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):


        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return redirect(request.META.get('HTTP_REFERER'))


class ValidarPermisoMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('login')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)

        #for permiso in self.get_perms():
        #    if request.user.has_perm(permiso):
        #        return super().dispatch(request, *args, **kwargs)


        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return redirect(request.META.get('HTTP_REFERER'))


