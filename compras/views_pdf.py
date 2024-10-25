from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def informe_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
    # Configuración de la página
    #page_width, page_height = landscape(letter)
    #c = canvas.Canvas(response, pagesize=(page_width, page_height))

    #page_width, page_height = 792, 612 # 11x8.5 inches at 72 dpi
    #c = canvas.Canvas(response, pagesize=(page_width, page_height))

    # Definimos las dimensiones de la página en formato horizontal
    page_width, page_height = 792, 612 # 11x8.5 inches at 72 dpi
    # Creamos un objeto Canvas con las dimensiones de la página en formato horizontal
    c = canvas.Canvas("horizontal.pdf", pagesize=(page_width, page_height))
    # Dibujamos un rectángulo en la página para comprobar su orientación


    #c.line(50, 50, 250, 50)

    # draw a vertical line
    #c.line(150, 100, 150, 200)

    # Encabezado
    c.setFont('Helvetica-Bold', 16)
    c.drawString(inch, page_height - inch, 'Informe en hoja de oficio')
    # Datos
    c.setFont('Helvetica', 12)
    c.drawString(inch, page_height - 2*inch, 'Fecha: 10 de mayo de 2023')
    c.drawString(inch, page_height - 3*inch, 'Autor: John Doe')
    c.drawString(inch, page_height - 4*inch, 'Contenido:')
    contenido = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                 'Pellentesque ut dolor mauris.']
    y = page_height - 5*inch
    for texto in contenido:
        c.drawString(inch, y, texto)
        y -= inch
    # Pie de página
    c.setFont('Helvetica-Oblique', 10)
    c.drawString(inch, inch, 'Este informe fue generado automáticamente por Django y ReportLab.')
    # Cerrar el PDF
    c.showPage()
    c.save()
    return response
