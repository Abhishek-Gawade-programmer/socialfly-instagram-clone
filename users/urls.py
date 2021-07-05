from django.urls import path
from .views import *
app_name='user'
urlpatterns = [
		path('profile/', profile, name='profile'),
		path('profile/<int:socialflyuser>/', profile, name='profile'),

		path('wants-follow/<int:socialflyuser>/', wants_follow, name='wants_follow'),
		path('profile-edit/', profile_edit, name='profile_edit'),
		path('home-page/', home_page, name='home_page'),
]