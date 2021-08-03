from django.urls import re_path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chats/(?P<room_name>\w+)/$',ChatConsumer.as_asgi()),
]