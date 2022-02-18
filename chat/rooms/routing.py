from django.urls import re_path
from .consumers import  chatconsumer




websocketurlpattern=[
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chatconsumer.as_asgi()),
]