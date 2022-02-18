from unicodedata import name
from django.shortcuts import render
from django.template import context
from .models import room
from django.http import JsonResponse
from django.contrib.auth import get_user_model

# Create your views here.

user=get_user_model()
def chat_room(request,*args,**kwargs):
    members_list=[]
    if (request.GET or None):
        room_name=request.GET.get('room_name')
        chat_room=room.objects.filter(name=room_name).first()
        room_name=chat_room.name
        members=user.objects.filter(room=chat_room).all()
        for member in members:
            members_list.append(member.username)
        response={
            'room_name':room_name,
            'members':members_list
        }
    return JsonResponse(response)
