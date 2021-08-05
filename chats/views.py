from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required



    
@login_required
def room(request, room_name=None):
    user_groups=Room.objects.filter(user_eligible__in=[request.user,])
    return render(request, 'chat.html', {
        'room_name_json': room_name,
        'username':request.user.username,
        'user_groups':user_groups
    })
