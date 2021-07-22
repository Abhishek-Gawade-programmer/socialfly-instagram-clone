from django.urls import path
from .views import *

app_name='posts'
urlpatterns = [
	path('explore/', explore, name='explore'),
	path('post-list-json-view/<int:num_posts>/', PostListJsonView.as_view(), name='post_list_json_view'),
	path('post-image-upload/', post_image_upload, name='post_image_upload'),
	path('post-submit/', submit_post, name='submit_post'),
	path('delete-post/', delete_post, name='delete_post'),

]