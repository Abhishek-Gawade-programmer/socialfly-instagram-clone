from django.urls import path
from .views import *
app_name='user'
urlpatterns = [
		path('home-page/', home_page, name='home_page'),

		path('profile/', profile, name='profile'),
		path('profile/<int:socialflyuser>/', profile, name='profile'),
		path('profile-edit/', profile_edit, name='profile_edit'),

		
		path('wants-follow-unfollow/', wants_follow_unfollow, name='wants_follow'),
		path('change-private-status/', change_private_status, name='change_private_status'),
]