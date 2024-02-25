"""
ASGI config for websocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket.settings')


from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application


from chatapp.middleware import TokenAuthMiddleware


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":
        TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
    ,
})
