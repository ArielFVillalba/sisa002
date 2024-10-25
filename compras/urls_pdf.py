from django.urls import path
from . import views_pdf

urlpatterns = [
    path('informe-pdf/', views_pdf.informe_pdf, name='informe_pdf'),


]
