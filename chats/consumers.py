import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models import Message
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):

    def fetch_messages(self,data):
        messages=Message.last_10_meassges()
        content={
            'message':messages.values()

        }

        print('fetch')
        self.send_message(content)

    def new_message(self,data):
        
        author=User.objects.get(username=data['from'])
        message=Message.objects.create(
            author=author,content=data['message']
            )

        message.save()
        content={
            'command':'new_message',
            'message':message.values()
        }
        self.send_chat_message(content)



    commands={
        'fetch_messages':fetch_messages,
        'new_message':new_message

    }


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)
        

    async def send_chat_message(self,message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))