from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse


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
def profile(request,socialflyuser=None):
    if socialflyuser:
        user_object = get_object_or_404(SocialflyUser, pk = socialflyuser)

    else:
        user_object = get_object_or_404(SocialflyUser, user = request.user)
    return render(request,'profile.html',{'user_object':user_object})


@login_required
def home_page(request):

    all_friends=SocialflyUser.objects.exclude( user = request.user)
    return render(request,'user_home.html',{'all_friends':all_friends})

@login_required
def profile_edit(request):
    user_object = get_object_or_404(SocialflyUser, user = request.user)
    user_from = UserEditFrom(request.POST or None,request.FILES or None, instance = user_object)

    if user_from.is_valid() :

        edit_user_from=user_from.save(commit=False)
        user_object.user.username=user_from.cleaned_data.get('username')
        user_object.user.first_name=user_from.cleaned_data.get('first_name')
        user_object.user.last_name=user_from.cleaned_data.get('last_name')
        user_object.user.email=user_from.cleaned_data.get('email')

        user_object.user.save()
        edit_user_from.save()
        messages.info(request, f" has been Updated successfully !!")
        return redirect("users:profile")

 
    return render(request, "edit-profile.html", {
                'user_from':user_from,
                'user_object':user_object})

@login_required
def wants_follow_unfollow(request):

    socialflyuser=request.POST.get('socialflyuser')
    who_receive_action = get_object_or_404(SocialflyUser, pk = socialflyuser)
    who_send_action = get_object_or_404(SocialflyUser, user = request.user)
    what_to_do={'action':False,'success':'true'}
    if who_receive_action.is_private:
        pass
    else:
        # follow the user
        if who_receive_action.allow_to_follow(who_send_action.pk):
            who_receive_action.followers.add(who_send_action.user)
            who_send_action.following.add(who_receive_action.user)
            what_to_do['action']='Unfollow'
            
        # unfollow the user
        else:

            who_receive_action.followers.remove(who_send_action.user)
            who_send_action.following.remove(who_receive_action.user)
            what_to_do['action']='Follow'

        who_send_action.save()
        who_receive_action.save()

        return JsonResponse(what_to_do,safe=False)


