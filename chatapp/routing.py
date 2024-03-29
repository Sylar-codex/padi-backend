# chat/routing.py
from django.urls import path
from .consumer import ChatConsumer, StartConnection, NotificationConsumer

websocket_urlpatterns = [
    path("", StartConnection.as_asgi()),
    path("notifications/", NotificationConsumer.as_asgi()),
    path("<conversation_name>/", ChatConsumer.as_asgi()),   
]
