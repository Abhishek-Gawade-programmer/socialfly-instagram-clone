from django.urls import path
from .views import *

app_name='posts'
urlpatterns = [
	path('post-image-upload/', post_image_upload, name='post_image_upload'),
	path('post-submit/', submit_post, name='submit_post'),
	path('delete-post/', delete_post, name='delete_post'),

]