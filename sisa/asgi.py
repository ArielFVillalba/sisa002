"""
ASGI config for sisa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

#import os

#from django.core.asgi import get_asgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisa.settings')

#application = get_asgi_application()

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path  # Asegúrate de importar esto
from sisa import consumers  # Importa tus consumidores de WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisa.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/print/", consumers.PrintConsumer.as_asgi()),  # Definición correcta de la ruta
        ])
    ),
})
