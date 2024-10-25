import csv
import json
import os
import django

# Establece el entorno de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisa.settings')
django.setup()

from contabilidad.models import Cuentacontable  # Asegúrate de que el nombre de tu app y modelo sean correctos

# Define la ruta completa del archivo JSON
#json_file_path = r'C:\Users\ariel\Documents\cuentas.json'
#json_file_path = r'C:\Users\ariel\Documents\python\sisa\sisa\contabilidad'
json_file_path = os.path.join(os.path.dirname(__file__), 'cuentas_exportadas.json')

# Asegúrate de que el archivo JSON existe
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"El archivo {json_file_path} no fue encontrado.")

# Abre y lee el archivo JSON
with open(json_file_path, 'r', encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)  # Carga el contenido del archivo JSON

# Recorrer cada elemento del archivo JSON y cargarlo en la base de datos
for item in data:
    # Crear una instancia del modelo `Cuentacontable` usando los datos del JSON
    Cuentacontable.objects.create(
        idempresa=1,
        idsucursal=1,
        cuenta=item.get('Cuenta'),
        denominacion=item.get('Denominación'),
        nivel=int(item.get('Nivel', 0)),  # Asigna 0 por defecto si 'Nivel' no está presente
        naturaleza=item.get('Naturaleza'),
        asentable=item.get('Asentable'),
        centro_costo=item.get('Centro Costo'),
        moneda=item.get('Moneda'),
        tipo_cambio=item.get('Tipo_cambio') if item.get('Tipo_cambio') else None,
        # Aquí puedes agregar más campos si es necesario
    )

print("Datos importados correctamente a la base de datos.")

