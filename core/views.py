from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def explore(request):
    return render(request,'explore.html')

