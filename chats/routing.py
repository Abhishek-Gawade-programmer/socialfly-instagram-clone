from .consumers import ChatConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/chats/(?P<room_name>\w+)/$',ChatConsumer.as_asgi()),
    re_path(r'ws/(?P<room_name>\w+)/$',ChatConsumer.as_asgi()),
]