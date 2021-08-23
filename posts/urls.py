from django.urls import path
from .views import *

app_name='posts'
urlpatterns = [
	path('explore/', explore, name='explore'),
	path('bookmark-post/', bookmark_post, name='bookmark_post'),
	path('post-image-upload/', post_image_upload, name='post_image_upload'),
	path('post-submit/', submit_post, name='submit_post'),
	path('delete-post/', delete_post, name='delete_post'),
	path('like-unlike-post/', like_unlike_post, name='like_unlike_post'),
	path('report-post/', report_post, name='report_post'),
	path('comment-post/', comment_on_post, name='comment_on_post'),
	path('post-detail/<slug>/<int:post_id>/',post_detail_view,name ='post_detail_view'),


]