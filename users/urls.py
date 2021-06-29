from django.urls import path
from .views import *
app_name='user'
urlpatterns = [
		path('profile/', profile, name='profile'),
		path('profile-edit/', profile_edit, name='profile_edit'),
]