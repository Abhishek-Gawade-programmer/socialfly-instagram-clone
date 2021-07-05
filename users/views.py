from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages


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

    all_friends=SocialflyUser.objects.exclude( user = request.user,following__in=[request.user,])
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
    else:
        print('jshabfhb',user_from.errors)

 
    return render(request, "edit-profile.html", {
                'user_from':user_from,
                'user_object':user_object})




@login_required
def wants_follow(request,socialflyuser):
    get_user = get_object_or_404(SocialflyUser, pk = socialflyuser)
    who_wants_follow = get_object_or_404(SocialflyUser, user = request.user)

    if get_user.is_private:
        pass
    else:
        get_user.followers.add(who_wants_follow.user)
        who_wants_follow.following.add(get_user.user)

        who_wants_follow.save()
        get_user.save()
        return redirect('users:profile')
        






