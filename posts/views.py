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
	return JsonResponse

@login_required
def delete_post(request):
	if  request.method == 'POST':
		post = get_object_or_404(Post, pk = request.POST.get('post_id'),user=request.user)
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
			if username:
				post.tagged_people.add(User.objects.get(username=username))
		post.posted=True
		post.save()
		return JsonResponse({'post':False})



@login_required
def explore(request):
	l=[report_post.post.id for report_post in ReportPost.objects.filter(user=request.user)]
	recommend_posts=Post.objects.filter(posted=True).exclude(id__in=l)

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


@login_required
def report_post(request):
	description=request.POST.get('description')
	post_id=request.POST.get('post_id')
	post = get_object_or_404(Post, pk = post_id)
	report_obj=ReportPost.objects.update_or_create(user=request.user,description=description,post=post)
	report_obj[0].save()
	return JsonResponse({'success':True})

@login_required
def comment_on_post(request):
	comment_text=request.POST.get('comment_text')
	post_id=request.POST.get('post_id')
	post = get_object_or_404(Post, pk = post_id)
	comment_obj=Comment.objects.create(text=comment_text,post=post,user=request.user)
	comment_obj.save()
	return render(request,'post_comment_ajax.html',
		{'commentlist':post.get_post_comments()[:3]})

@login_required
def like_unlike_post(request):
	post_id=request.POST.get('post_id')
	post = get_object_or_404(Post, pk = post_id)
	if request.user in  post.like_people.all():
		post.like_people.remove(request.user)
		action='unlike'
	else:
		post.like_people.add(request.user)
		action='like'
	return JsonResponse({'success':True,"action":action,'num_likes':post.get_number_like()},safe=False)


@login_required
def post_detail_view(request,slug,post_id):
    post = get_object_or_404(Post, pk = post_id,slug=slug)
    return render(request,'post_detail.html',{'post':post})
