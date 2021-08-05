from django.contrib import admin

from chats.models import Message,Room
admin.site.register(Message)
admin.site.register(Room)
