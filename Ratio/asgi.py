"""
ASGI config for Ratio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ratio.settings')

application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

import apps.chat.routing


application = ProtocolTypeRouter(
    {
        "http":asgi_app,
        "websocket":AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(apps.chat.routing.websocket_urlpatterns))
        )
    }
)
