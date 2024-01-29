# chat/routing.py
from django.urls import path
from .consumer import ChatConsumer

websocket_urlpatterns = [
    path("<conversation_name>/", ChatConsumer.as_asgi())
    # re_path(r"ws/chatapp/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
]
