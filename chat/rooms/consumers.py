import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class chatconsumer(WebsocketConsumer):
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
        message=data['message']
        self.send_message_to_group(message)

        


    def send_message_to_group(self,message):

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )



    def chat_message(self,message):
        self.send(text_data=json.dumps({
          'message':message
        }))    