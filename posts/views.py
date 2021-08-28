from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.db.models import Q
from django.conf import settings
from .models import *

from django.core.exceptions import ObjectDoesNotExist


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
		usernames_list=form_data.get('tag_usernames')
		usernames_list=usernames_list.split(',')[:-1]
		for username in usernames_list:
			user_from_username=User.objects.get(username=username)
			post.tagged_people.add(user_from_username)
			post_activity_fuc(reason="tagged user",
			changed_by=user_from_username,post=post)
		

		post.posted=True

		post.save()
		post_activity_fuc(reason="created new post",
				changed_by=request.user,post=post)


 	
		return JsonResponse({'post':False})



@login_required
def explore(request):
	l=[report_post.post.id for report_post in ReportPost.objects.filter(user=request.user)]
	recommend_posts=Post.objects.filter(
		Q(posted=True),
		Q(user__in=request.user.get_social_user.following.all())|
		Q(user=request.user)
		).exclude(id__in=l)

	page = request.GET.get('page', 1)
	paginator = Paginator(recommend_posts, 2)
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
	post_activity_fuc(reason="post report",
				changed_by=request.user,post=post)
	post.save()
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
	post.save()
	post_activity_fuc(reason="comment added",
				changed_by=request.user,post=post)

	return render(request,'post_comment_ajax.html',
		{'commentlist':post.get_post_comments()[:3]})

@login_required
def like_unlike_post(request):
	post_id=request.POST.get('post_id')
	post = get_object_or_404(Post, pk = post_id)
	if request.user in  post.like_people.all():
		post.like_people.remove(request.user)
		action='unlike'
		try:
			pa_obj=PostActivity.objects.get(
				Q(reason__contains="unlike post")|
                Q(reason__contains="like post"),
				changed_by=request.user,
				post=post)
			pa_obj.reason='unlike post'
			pa_obj.save()
		except ObjectDoesNotExist:
			post_activity_fuc(reason="unlike post",
				changed_by=request.user,post=post)

	else:
		post.like_people.add(request.user)
		action='like'

		try:
			pa_obj=PostActivity.objects.get(
				Q(reason__contains="unlike post")|
                Q(reason__contains="like post"),
				changed_by=request.user,
				post=post)
			pa_obj.reason='like post'
			pa_obj.save()
		except ObjectDoesNotExist:
			post_activity_fuc(reason="like post",
				changed_by=request.user,post=post,)
	post.save()
	return JsonResponse({'success':True,"action":action,'num_likes':post.get_number_like()},safe=False)


@login_required
def bookmark_post(request):
	post_id=request.POST.get('post_id')
	post = get_object_or_404(Post, pk = post_id)
	if request.user in  post.bookmark_user.all():
		post.bookmark_user.remove(request.user)
		action=True
	else:
		post.bookmark_user.add(request.user)
		action=False
	post.save()
	return JsonResponse({'success':True,"action":action},safe=False)


@login_required
def post_detail_view(request,slug,post_id):
    post = get_object_or_404(Post, pk = post_id,slug=slug)
    return render(request,'post_detail.html',{'post':post})

def post_activity_fuc(reason,changed_by,post):
	pa_obj=PostActivity.objects.create(
			reason=reason,
			changed_by=changed_by,
			post=post)
	pa_obj.save()
	return 
