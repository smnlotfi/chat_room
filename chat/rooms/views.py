from unicodedata import name
from django.shortcuts import render
from django.template import context
from .models import room
from django.http import JsonResponse, response
from django.contrib.auth import get_user_model

# Create your views here.

user_model=get_user_model()

def chat_room(request,*args,**kwargs):
    members_list=[]
    if (request.GET or None):
        current_user_name=request.user.username
        room_name=request.GET.get('room_name')
        chat_room=room.objects.filter(name=room_name).first()
        room_name=chat_room.name
        members=user_model.objects.filter(room=chat_room).all()
        for member in members:
            members_list.append(member.username)
        response={
            'room_name':room_name,
            'members':members_list,
            'current_user':current_user_name
        }
    return JsonResponse(response)


def createnewroom(request,*args,**kwargs):
    if(request.POST or None):
        RoomName=request.POST.get('RoomName')
        createroom=room.objects.create(name=RoomName,admin=request.user.username)
        createroom.members.add(request.user)
        response={'msg':'room is created','roomname':createroom.name}
    else:
        response={'msg':'na2nestam'}

    print(response)

    return JsonResponse(response)
    

