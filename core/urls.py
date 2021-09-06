from django.urls import path,include
from .views import *
from django.views.generic import TemplateView
app_name='core'
urlpatterns = [
	path('webpush/', include('webpush.urls')),
	path('send_push', send_push),
	path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
	path('home/', home, name='home'),

]