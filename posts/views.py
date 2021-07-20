from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *

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
	context={'recommend_posts':recommend_posts}
	return render(request,'explore.html',context)