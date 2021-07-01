from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.dispatch import receiver
import requests
from django.core import files
from io import BytesIO

from .forms import *
from .models import *

#USER AUTHENTICATION 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount






@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    extra_data=user.socialaccount_set.filter(provider='google')[0].extra_data
    resp = requests.get(extra_data['picture'])
    fp = BytesIO()
    fp.write(resp.content)
    file_name = extra_data['picture'].split("/")[-1]
    socialflyuser = SocialflyUser.objects.create(user=user)
    socialflyuser.profile_photo.save(user.username+'profile_photo.png', files.File(fp))

    socialflyuser.save()
    return redirect('user:profile_edit')







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
    user_object = get_object_or_404(SocialflyUser, user = request.user)
    return render(request,'profile.html',{'user_object':user_object})


@login_required
def profile_edit(request):
    # return render(request,'edit-profile.html')
    user_object = get_object_or_404(SocialflyUser, user = request.user)
    user_from = UserEditFrom(request.POST or None,request.FILES or None, instance = user_object)

    if user_from.is_valid() :

        edit_user_from=user_from.save(commit=False)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',user_from.cleaned_data)
        user_object.user.username=user_from.cleaned_data.get('username')
        user_object.user.first_name=user_from.cleaned_data.get('first_name')
        user_object.user.last_name=user_from.cleaned_data.get('last_name')
        user_object.user.email=user_from.cleaned_data.get('email')

        user_object.user.save()
        edit_user_from.save()
        messages.info(request, f" has been Updated successfully !!")
        return redirect("users:profile")
    else:
        print('jshabfhb',user_from.errors)

 
    return render(request, "edit-profile.html", {
                'user_from':user_from,
                'user_object':user_object})

