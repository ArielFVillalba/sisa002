from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import render, redirect
from django.shortcuts import render


class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        try:
            return super().process_view(request, callback, callback_args, callback_kwargs)
        except CsrfViewMiddleware().reject:
            return redirect('login')  # Redirigir a la página de inicio de sesión

def error_404_view(request, exception):
    return redirect('login')

def csrf_error(request, reason=""):
    errors=" intente denuevo "
    return render(request, 'base/login.html', {'messages': errors})
