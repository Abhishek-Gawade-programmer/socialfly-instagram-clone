from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse


from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat 


from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import *
from posts.models import Post,PostActivity
from chats.models import Room
from itertools import chain

#USER RECOMMANDATION
from .user_ranking import UserRanking

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#USER AUTHENTICATION  

from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required


from django.conf import settings
from django.views.decorators.http import require_GET, require_POST



class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'account/signup.html'


    def form_valid(self, form):
        user = form.save()
        login(self.request, user,backend='allauth.account.auth_backends.AuthenticationBackend')
        return redirect('posts:explore')



@login_required
def profile(request,socialflyuser=None):
    from io import BytesIO



    if socialflyuser:
        user_object = get_object_or_404(SocialflyUser, pk = socialflyuser)

    else:
        user_object = get_object_or_404(SocialflyUser, user = request.user)

    user_followers=user_object.followers.all()
    user_followings=user_object.following.all()

    return render(request,'profile.html',{'user_object':user_object,
                                    'user_followers':user_followers,
                                    'user_followings':user_followings,
                                    })




@login_required
def home_page(request):
    all_friends=SocialflyUser.objects.exclude( user = request.user)
    obj=UserRanking(request.user.get_social_user)
    return render(request,'user_home.html',{'all_friends':obj.arrange_the_users()})

@require_POST
@login_required
def upload_profile_picture(request):
    user_object = get_object_or_404(SocialflyUser, user = request.user)
    user_object.profile_photo=request.FILES.get('image')
    user_object.save()
    from easy_thumbnails.files import get_thumbnailer
    options = {'size': (152, 150), 'crop': True}
    thumb_url = get_thumbnailer(user_object.profile_photo).get_thumbnail(options).url

    return JsonResponse({'uploaed':True,'image_url':thumb_url},safe=False)





@require_POST
@login_required
def user_genuine_info(request):
    try:
        genuine_user=GenuineUser.objects.get(user=request.user)
        genuine_user.description=request.POST.get('genuine_description')
        genuine_user.save()
    except ObjectDoesNotExist:
        obj=GenuineUser.objects.create(
            user=request.user,
            description=request.POST.get('genuine_description'),
            )
        obj.save()    

    messages.info(request, 'Account Genuine  request has been successfully Deleted !!')
    return JsonResponse({'form_saved':True},safe=False)




@require_POST
@login_required
def delete_user(request):
    print('delting user')
    for _ in request.user.get_social_user.get_user_rooms():
        _.delete()
    
    request.user.delete()
    logout(request)
    messages.info(request, 'Account successfully Deleted !!')
    return JsonResponse({'delete':True},safe=False)





@login_required
def profile_edit(request):
    user_object = request.user.get_social_user
    user_from = UserEditFrom(request.POST or None,request.FILES or None, instance = user_object)

    if user_from.is_valid() :

        edit_user_from=user_from.save(commit=False)
        user_object.user.username=user_from.cleaned_data.get('username')
        user_object.user.first_name=user_from.cleaned_data.get('first_name')
        user_object.user.last_name=user_from.cleaned_data.get('last_name')
        user_object.user.email=user_from.cleaned_data.get('email')

        user_object.user.save()
        edit_user_from.save()
  
        messages.info(request, f"Your Profile has been Updated successfully !!")
        return redirect("users:profile")

 
    return render(request, "edit-profile.html", {
                'user_from':user_from,
                })














@login_required
def wants_follow_unfollow(request):
    socialflyuser=request.POST.get('socialflyuser')
    who_receive_action = get_object_or_404(SocialflyUser, pk = socialflyuser)
    who_send_action = request.user.get_social_user
    what_to_do={'action':False,'success':'true'}

    if who_receive_action.is_private:
        pass
    else:
        # follow the user
        if who_receive_action.allow_to_follow(who_send_action.pk):
            who_receive_action.followers.add(who_send_action.user)
            #notification of user for following
            who_send_action.following.add(who_receive_action.user)
            try:
                ua_obj=UserActivity.objects.get(
                    Q(reason__contains="started following you")|
                    Q(reason__contains="unfollow you"),
                    changed_by=who_send_action.user,
                    user_target=who_receive_action.user,)
                ua_obj.reason='started following you'
                ua_obj.save()
            except ObjectDoesNotExist:
                user_activity_fuc("started following you",
                    who_receive_action.user,
                    who_send_action.user)
            

            what_to_do['action']='Unfollow'
       
            
        # unfollow the user
        else:
             #notification of user for following
            who_receive_action.followers.remove(who_send_action.user)
            who_send_action.following.remove(who_receive_action.user)
            what_to_do['action']='Follow'

            try:
                ua_obj=UserActivity.objects.get(
                    Q(reason__contains="started following you")|
                    Q(reason__contains="unfollow you"),
                    changed_by=who_send_action.user,
                    user_target=who_receive_action.user,)
                ua_obj.reason='unfollow you'
                ua_obj.save()
            except ObjectDoesNotExist:
                user_activity_fuc("unfollow you",
                    who_receive_action.user,
                    who_send_action.user)
        who_send_action.save()
        who_receive_action.save()
        add_remove_people_chat(
                user1=who_receive_action.user,
                user2=who_send_action.user,
                )

        return JsonResponse(what_to_do,safe=False)



@login_required
def change_private_status(request):
    socialflyuser =  request.user.get_social_user
    if socialflyuser.is_private:
        socialflyuser.is_private=False
        socialflyuser._change_reason='private settings off'
    else:
        socialflyuser.is_private=True
        socialflyuser._change_reason='private settings on'
    socialflyuser.save()
    return JsonResponse({'success':'true'},safe=False)


@login_required
def search_results(request):
    if request.is_ajax():
        string_to_search=request.POST.get('string_to_search')
        qs=User.objects.exclude(username=request.user.username).annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
                ).filter(   
                    Q(username__icontains=string_to_search)|
                    Q(full_name__icontains=string_to_search) | 
                    Q(first_name__icontains=string_to_search) | 
                    Q(last_name__icontains=string_to_search)
                )
        data=[]
        for i in qs:
            item={
            'full_name':i.first_name+' '+i.last_name,
            'username':i.username,
            'profile_image':i.get_social_user.profile_photo.url,
            'is_genuine':i.is_genuine,
            'url':i.get_social_user.get_absolute_url()

            }
            data.append(item)

        data_of_search={'data':data}
        return JsonResponse(data_of_search,safe=False)

@login_required
def user_actions(request):
    x=PostActivity.objects.first()

    print(request.user.date_joined,type(request.user.date_joined))
    print(x.updated,type(x.updated))

    notifiy_on_post=PostActivity.objects.filter(
        Q(post__user=request.user)& ~Q(reason="tagged user")
         |Q(changed_by=request.user)&Q(reason='tagged user')
        |Q(changed_by__in=request.user.get_social_user.following.all())
            &Q(reason='created new post')
        ).exclude(Q(changed_by=request.user),
        Q(reason="comment added")|Q(reason="like post")|Q(reason="created new post"),
        ).exclude(
        Q(updated__lt=request.user.date_joined))


    notifiy_on_user=UserActivity.objects.filter(user_target=request.user)
    # following_post=Post.objects.filter(user__in=request.user.get_social_user.following.all())
    all_notifiactions=list(notifiy_on_post)+list(notifiy_on_user)#+list(following_post)
    all_notifiactions.sort(
        key=lambda item: item.updated,
        reverse=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(all_notifiactions, 5)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        numbers = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(request,'user_activity_notification.html',{'numbers': numbers})

    context={'all_notifiactions':all_notifiactions,
              'numbers': numbers}
    return render(request,'user_activity.html',context)



def add_remove_people_chat(user1,user2):
    if (user2 in  user1.get_social_user.following.all()) and (user1 in user2.get_social_user.following.all()):
        for room in Room.objects.all():
            if room.get_user_set()!={user1,user2}:
                obj=Room.objects.create()
                obj.user_eligible.add(*[user1,user2])
                obj.save()
                return 
    else:
        for room in Room.objects.all():
            if room.get_user_set()=={user1,user2}:
                room.delete()
        return         
         

def user_activity_fuc(reason,user_target,changed_by):
    ua_obj=UserActivity.objects.create(
        reason=reason,
        user_target=user_target,
        changed_by=changed_by)
    ua_obj.save()
    return 

