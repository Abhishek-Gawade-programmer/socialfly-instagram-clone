from django.contrib import admin
from users.models import *
from posts.models import *
from simple_history.admin import SimpleHistoryAdmin


admin.site.register(Post,SimpleHistoryAdmin)
admin.site.register(PostImage)
admin.site.register(User,SimpleHistoryAdmin)
admin.site.register(SocialflyUser,SimpleHistoryAdmin)

# Register your models here.
