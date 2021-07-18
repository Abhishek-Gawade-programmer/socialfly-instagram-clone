from django.shortcuts import render
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
	return JsonResponse({'post':False})
