from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message,Room,UserRoomInfo
from users.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ChatConsumer(WebsocketConsumer):

    def fetch_messages_of_room(self, room_id,page_no=None):
        if not page_no:
            messages = Message.last_10_messages(room_id)
            content = {
                'command': 'room_message',
                'room_id':room_id,
                'messages': self.messages_to_json(messages)
            }
        else:
            messages_all = Message.objects.filter(room__str_id=room_id)
            paginator = Paginator(messages_all, 10)
            try:
                print('OKAY')
                messages = paginator.page(page_no)
                content = {
                    'command': 'room_message_add',
                    'room_id':room_id,
                    'messages': self.messages_to_json(messages)
                }
            except (PageNotAnInteger,PageNotAnInteger,EmptyPage):
                print('ERROR')
                content = {
                    'command': 'room_message_na',
                    'room_id':room_id,
                }
        self.send_message(content)

    def new_message(self, data):

        author_user = get_object_or_404(User,username=self.scope["user"].username)
        get_room=get_object_or_404(Room,str_id=data['room_id'])
        useroominfo=get_object_or_404(UserRoomInfo,
            room=get_room,user=author_user)

        message = Message.objects.create(
            user=author_user, 
            content=data['message'],
            room=get_room,
            )

        content = {
            'command': 'new_message_save_db',
            'room_id':message.room.str_id,
            'message': self.message_to_json(message),
            'message_counter': useroominfo.get_unseen_message()
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        
        return {
            'author': message.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp.strftime( "%I %p|%d %b %y")),
            'room_name': message.room.str_id,
            'profile_photo':message.user.get_social_user.profile_photo.url
        }

    def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            self.accept()
            curent_user = get_object_or_404(User,
                username=self.scope["user"].username)
            user_groups=Room.objects.filter(user_eligible__in=[curent_user,])
            for user_group in user_groups:
                async_to_sync(self.channel_layer.group_add)(
                    user_group.str_id,
                    self.channel_name,
                )


        #user chat session start
        self.send(text_data=json.dumps({'START session':'we are connected'}))


    def disconnect(self, close_code):
        curent_user = get_object_or_404(User,
                username=self.scope["user"].username)
        user_groups=Room.objects.filter(user_eligible__in=[curent_user,])
        for user_group in user_groups:
            async_to_sync(self.channel_layer.group_discard)(
                user_group.str_id,
                self.channel_name,
            )
        
        self.send(text_data=json.dumps({'END session':'we are disconnected'}))
        #user chat session send

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['command']=='messages_of_that_room':
            self.room_group_name=data['room_id']
            if data.get('previous_room'):
                self.update_last_seen(data.get('previous_room'))
            self.update_last_seen(data['room_id'])
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name,
            )
            self.fetch_messages_of_room(data['room_id'])
        elif data['command']=='messages_of_that_room_scroll':
            self.fetch_messages_of_room(data['room_id'],data['page_no'])
            print('DATA is',data)
        
        elif data['command'] == 'new_message':
            print('new message from user ',data,self.scope["user"])
            self.new_message(data)

        

    def send_chat_message(self, message):   
          async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
             {
                'type': 'chat_message',
                'message': message
            })
                     
        

    def send_message(self, message):

        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        print('WELCOM TO CHART MESSAGE',event)
        message = event['message']
        self.send(text_data=json.dumps(message))

    def update_last_seen(self,room_str_id):
        get_room=get_object_or_404(Room,str_id=room_str_id)
        curent_user = get_object_or_404(User,
                username=self.scope["user"].username)

        try:
            user_room_info_obj=UserRoomInfo.objects.get(room=get_room, 
                user=curent_user)
        except ObjectDoesNotExist:
            user_room_info_obj=UserRoomInfo.objects.create(room=get_room, 
                user=curent_user)
        user_room_info_obj.last_seen=timezone.now()
        user_room_info_obj.save()


