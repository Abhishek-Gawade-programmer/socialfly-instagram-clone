from django.urls import path
from .views import *
app_name='core'
urlpatterns = [
		path('explore/', explore, name='explore'),
]