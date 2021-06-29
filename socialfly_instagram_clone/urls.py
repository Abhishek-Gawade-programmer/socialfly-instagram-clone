from django.contrib import admin
from django.urls import path,include

from django.contrib.auth import views
from users.views import UserSignUpView

# from users.forms import UserLoginForm


urlpatterns = [
    path('admin/', admin.site.urls),
     path('accounts/signup/',UserSignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', include('core.urls',namespace='core')),
    path('users/', include('users.urls',namespace='users')),
]
