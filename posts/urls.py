from django.urls import path
from .views import *

app_name='posts'
urlpatterns = [
	path('post-image-upload/', post_image_upload, name='post_image_upload'),

]