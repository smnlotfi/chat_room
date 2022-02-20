import imp
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import message,room
from chat.serializer import message_serializer
from rest_framework.renderers import JSONRenderer

class chatconsumer(WebsocketConsumer):

    def send_message(self,data):
        pass

    def fetch_message(self,data):
        room_name=data['room_name']
        chat_room=room.objects.filter(name=room_name).first()
        messages=message.objects.filter(related_group=chat_room).order_by('-message_send_time').all()
        messages=self.data_serializer(messages)
        self.chat_message(eval(messages))









    def data_serializer(self,data):
        data=message_serializer(data,many=True)
        data=JSONRenderer().render(data.data)
        return data
    commands={
        'fetch_message':fetch_message,
        'send_message':send_message
    }
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
        # message=data['message']
        # self.send_message_to_group(message)

        


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