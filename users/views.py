from django.shortcuts import render,get_object_or_404,redirect
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
    template_name = 'account/signup.html'


    def form_valid(self, form):
        user = form.save()
        login(self.request, user,backend='allauth.account.auth_backends.AuthenticationBackend')
        return redirect('core:explore')

@login_required
def profile(request):
    return render(request,'profile.html')



@login_required
def profile_edit(request):
    # return render(request,'edit-profile.html')
    user_object = get_object_or_404(SocialflyUser, user = request.user)
    user_from = UserEditFrom(request.POST or None, 
        instance = user_object)
    if user_from.is_valid() and user_edit_from.is_valid():
        edit_user_from=user_from.save(commit=False)
        user_from.save()
        edit_user_from.save()
        messages.info(request, f" has been Updated successfully !!")
        return redirect("users:profile")

 
    return render(request, "edit-profile.html", {
                'user_from':user_from,
                # 'user_edit_from':user_edit_from,
                'user_object':user_object})

