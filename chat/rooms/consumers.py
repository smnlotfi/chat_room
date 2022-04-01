import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import message,room
from chat.serializer import message_serializer,user_serializer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model

user=get_user_model()


class chatconsumer(WebsocketConsumer):


    def send_message(self,data):
        room_name=data['room_name']
        content=data['message']
        author=data['author']
        author=user.objects.filter(username=author).first()
        chat_room=room.objects.filter(name=room_name).first()
        new_message=message.objects.create(author=author,related_group=chat_room,content=content)

        data={
            'command':'new_message',
            'data':eval(self.message_serializer(new_message))
        }

        self.send_message_to_group(data)
    


# ......................................................

    
    def chat_open(self,data):
        username=data['username']
        room_name=data['room_name']
        users=user.objects.exclude(username=username)
        chat_room=room.objects.filter(name=room_name).first()
        room_admin=chat_room.admin
        members=chat_room.members.all().exclude(username=username)
        messages=message.objects.filter(related_group=chat_room).order_by('-message_send_time').all()
        data={
            'command':'chat_open',
            'data':eval(self.message_serializer(messages)),
            'room_admin':room_admin,
            'users':eval(self.user_serializer(users)),
            'members':eval(self.user_serializer(members)),
        }
        self.chat_message(data)



# ......................................................




    def addremove_members(self,data):
        username=data['username']
        roomname=data['room']
        mission=data['mission']
        elementid=data['elementid']
        if(mission=='add'):
            targetroom=room.objects.filter(name=roomname).first()
            targetuser=user.objects.filter(username=username).first()
            targetroom.members.add(targetuser)
            response={'result':'add'}
        elif(mission=='remove'):
            targetroom=room.objects.filter(name=roomname).first()
            targetuser=user.objects.filter(username=username).first()
            targetroom.members.remove(targetuser)
            response={'result':'remove'}

        data={
            'result':response,
            'command':'addremove_members',
            'elementid':elementid,
            'room':roomname,
            'user':username
        }

        self.chat_message(data)
        
        
# ......................................................
        


    def message_serializer(self,data): 
        serilized=message_serializer(data,many=(lambda data:True if (data.__class__.__name__=='QuerySet') else False)(data))
        data=JSONRenderer().render(serilized.data)
        return data

    def user_serializer(self,data): 
        serilized=user_serializer(data,many=(lambda data:True if (data.__class__.__name__=='QuerySet') else False)(data))
        data=JSONRenderer().render(serilized.data)
        return data




    commands={
        'chat_open':chat_open,
        'send_message':send_message,
        'addremove_members':addremove_members
    }






# ......................................................




    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        return self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):
        data=json.loads(text_data)
        command=data['command']
        self.commands[command](self,data)


        


    def send_message_to_group(self,message):
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )



    def chat_message(self,message):
        self.send(text_data=json.dumps({
          'message':message
        }))    









class general(WebsocketConsumer):
    
    
    def connect(self):
        self.public = self.scope['url_route']['kwargs']['public']
        self.room_group_name = f'public_{self.public}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        return self.accept()


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )



    def receive(self, text_data):
        data=json.loads(text_data)
        self.send_message_to_group(data)




    def send_message_to_group(self,message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )



    def chat_message(self,message):
        self.send(text_data=json.dumps({
          'message':message
        })) 