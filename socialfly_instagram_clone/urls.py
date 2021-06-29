from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static 
from django.contrib.auth import views
from users.views import UserSignUpView

# from users.forms import UserLoginForm
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
     path('accounts/signup/',UserSignUpView.as_view(), name='signup'),
     path('accounts/', include('allauth.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),

    path('', include('core.urls',namespace='core')),
    path('users/', include('users.urls',namespace='users')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
