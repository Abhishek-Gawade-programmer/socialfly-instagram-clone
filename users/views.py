from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import *
from .models import *

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
        return redirect('login')





@login_required
def profile(request):
    return render(request,'profile.html')


