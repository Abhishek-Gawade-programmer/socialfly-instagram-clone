from django.urls import path,include
from .views import *

app_name='users'
urlpatterns = [
		path('home-page/', home_page, name='home_page'),
		path('your-notification/', user_actions, name='user_actions'),
		path('delete-user/', delete_user, name='delete_user'),
		path('profile/', profile, name='profile'),
		path('profile/<int:socialflyuser>/', profile, name='profile'),
		path('profile-edit/', profile_edit, name='profile_edit'),
		path('search-results/', search_results, name='search_results'),

		path('user-genuine-info/', user_genuine_info, name='user_genuine_info'),

		path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
		path('wants-follow-unfollow/', wants_follow_unfollow, name='wants_follow'),
		path('change-private-status/', change_private_status, name='change_private_status'),


]