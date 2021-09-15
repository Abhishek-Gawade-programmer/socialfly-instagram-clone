from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static 
from django.contrib.auth import views
from users.views import UserSignUpView
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/',UserSignUpView.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='landing_page.html'),name='landing_page'),
    path('', include('core.urls',namespace='core')),
    path('', include('pwa.urls')),
    path('users/', include('users.urls',namespace='users')),
    path('posts/', include('posts.urls',namespace='posts')),
    path('chats/', include('chats.urls',namespace='chats')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
