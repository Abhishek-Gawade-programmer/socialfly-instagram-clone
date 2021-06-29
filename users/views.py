from django.shortcuts import render
from django.views.generic import CreateView
from django.shortcuts import redirect

from .forms import *
from .models import *
#USER AUTHENTICATION 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'

    # def get_context_data(self, **kwargs):
    #     kwargs['user_type'] = 'Student'
    #     return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:explore')





@login_required
def profile(request):
    return render(request,'profile.html')


