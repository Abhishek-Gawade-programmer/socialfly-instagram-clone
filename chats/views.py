from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


@login_required
def all_friends_chats(request):
    return render(request,'chat.html')
@login_required
def index(request):
    return render(request, 'index.html')

def room(request, room_name):
    print('jkasnd')
    return render(request, 'room.html', {
        'room_name': room_name
    })