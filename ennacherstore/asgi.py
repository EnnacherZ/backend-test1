"""
ASGI config for ennacherstore project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from store import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ennacherstore.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Ajouter vos routes WebSocket ici, si nécessaire
        ])
    ),
    "http.request": URLRouter([
        path("events/shoe_sizes/", consumers.SSEConsumer.as_asgi()),  # SSE route
    ]),
})