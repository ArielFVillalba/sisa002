import json
import os
import django

# Establece el entorno de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisa.settings')
django.setup()

from contabilidad.models import Cuentacontable  # Asegúrate de que el nombre de tu app y modelo sean correctos

# Define la ruta completa del archivo JSON
json_file_path = os.path.join(os.path.dirname(__file__), 'cuentas_exportadas_soloacentables.json')

# Obtener todos los objetos del modelo `Cuentacontable`
#cuentas = Cuentacontable.objects.all()
cuentas = Cuentacontable.objects.filter(asentable='SI',idempresa=1)

# Crear una lista de diccionarios con los datos que deseas exportar
data = []
for cuenta in cuentas:
    data.append({
        'Cuenta': cuenta.cuenta,
        'Denominación': cuenta.denominacion,
        'Nivel': cuenta.nivel,
        'Naturaleza': cuenta.naturaleza,
        'Asentable': cuenta.asentable,
        'Centro Costo': cuenta.centro_costo,
        'Moneda': cuenta.moneda,
        'Tipo_cambio': cuenta.tipo_cambio,
        # Agrega aquí los demás campos que desees exportar
    })

# Escribir los datos en el archivo JSON
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

print(f"Datos exportados correctamente a {json_file_path}")
