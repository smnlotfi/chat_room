from django.urls import re_path
from .consumers import  chatconsumer,general




websocketurlpattern=[
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chatconsumer.as_asgi()),
    re_path(r'ws/public/(?P<public>\w+)/$', general.as_asgi()),
]