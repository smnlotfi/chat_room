from django.urls import path,include
from .views import chat_room,createnewroom



urlpatterns = [
    path('chat/<str:chat_room>',chat_room,name='chat_room'),
    path('newroom',createnewroom,name='newroom'),
]