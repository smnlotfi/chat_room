import imp
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rooms.models import room
from django.contrib.auth import get_user_model



user=get_user_model()



@login_required(login_url='/')
def chat(request):
    rooms_name=[]
    rooms=room.get_all_room(room)
    for chat_room in rooms:
        members=user.objects.filter(room=chat_room)
        for member in members:
            if member==request.user:
                rooms_name.append(chat_room.name)
     
    context={
        'rooms_name':rooms_name
    }
    return render(request,'chat.html',context)