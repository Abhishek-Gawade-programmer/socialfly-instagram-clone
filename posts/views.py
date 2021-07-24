from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from django.conf import settings
from .models import *


#PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger







@login_required
def post_image_upload(request):
	# print(request.FILES,request.method)
	if  request.method == 'POST':
		new_post=Post.objects.create(user=request.user)

		for _ in request.FILES:
			post_image=PostImage.objects.create(
				image=request.FILES.get(_),
				post=new_post
				)
			post_image.save()
		new_post.save()
		return JsonResponse({'success':True,'post_pk':new_post.pk},safe=False)
	return JsonResponse({'success':False})



@login_required
def delete_post(request):
	# print(request.FILES,request.method)
	if  request.method == 'POST':
		post = get_object_or_404(Post, pk = request.POST.get('post_pk'))
		post.delete()
		return JsonResponse({'success':True},safe=False)
	return JsonResponse({'post':False})

@login_required
def submit_post(request):
	if  request.method == 'POST':
		form_data=request.POST

		post = get_object_or_404(Post, pk = form_data.get('post_pk'))
		post.caption=form_data.get('caption_text')
		usernames_list=form_data.get('tag_usernames_list').split(',')
		for username in usernames_list:
			post.tagged_people.add(User.objects.get(username=username))
		post.posted=True
		post.save()
		return JsonResponse({'post':False})



@login_required
def explore(request):
	recommend_posts=Post.objects.filter(posted=True)
	page = request.GET.get('page', 1)
	paginator = Paginator(recommend_posts, 1)
	try:
		numbers = paginator.page(page)
	except PageNotAnInteger:
		numbers = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			# If the request is AJAX and the page is out of range
			# return an empty page
			return HttpResponse('')
		# If page is out of range deliver last page of results
		numbers = paginator.page(paginator.num_pages)


	context={'recommend_posts':recommend_posts,
			  'numbers': numbers}
	if request.is_ajax():
		return render(request,'post_ajax.html',context)
	return render(request,'explore.html',context)









class PostListJsonView(View):
	def get(self,*args,**kwargs):
		upper=kwargs.get('num_posts')#3
		lower=upper-2
		recommend_posts=list(Post.objects.filter(posted=True).values(
			'user__username','user__first_name','user__last_name',
			"user__socialflyuser__profile_photo",
			"caption", "created", "id", "like_people", "posted",
			  "updated", "user_id",
			)[lower:upper])
		for post in recommend_posts:
			post["tagged_people"]=list(
					get_object_or_404(
						Post, id =post['id']).tagged_people.all().values(
							'first_name','last_name','username'))
			post_user=User.objects.get(id=post["user_id"]).get_social_user
			post['profile_photo']=post_user.profile_photo.url
			post['get_absolute_url']=post_user.get_absolute_url()
	
			post['post_images']=list(PostImage.objects.filter(post__id=post['id']).values())
			for post_image in post['post_images']:
				post_image['image']=settings.MEDIA_URL+post_image['image']
		return JsonResponse({'data':recommend_posts},safe=False)

