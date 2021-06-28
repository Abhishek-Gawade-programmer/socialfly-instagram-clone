from django.contrib import admin
from users.models import *

admin.site.register(User)
admin.site.register(SocialflyUser)

# Register your models here.
