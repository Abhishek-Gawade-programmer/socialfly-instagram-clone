from django.urls import path
from .views import *
app_name='chats'
urlpatterns = [
	path('', index, name='index'),
	path('all-friends-chats/', all_friends_chats, name='all_friends_chats'),
	path('<str:room_name>/', room, name='room'),
]