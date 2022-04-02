from django.urls import path,include
from .views import chat_room,createnewroom,searchmember



urlpatterns = [
    path('chat/<str:chat_room>',chat_room,name='chat_room'),
    path('newroom',createnewroom,name='newroom'),
    path('searchmember',searchmember,name='searchmember'),
]