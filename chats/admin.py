from django.contrib import admin

from chats.models import Message,Room,UserRoomInfo
admin.site.register(Message)
admin.site.register(UserRoomInfo)
admin.site.register(Room)
