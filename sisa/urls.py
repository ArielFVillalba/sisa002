
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')),
    #path('', include('marketing.urls')),
    #path('', include('inventario.urls')),
    path('', include('compras.urls')),
    path('', include('ventas.urls')),
    path('', include('stock.urls')),
    path('', include('caja.urls')),
    path('', include('contabilidad.urls')),
    path('*',RedirectView.as_view(url='/login/', permanent=False)),
    # ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

