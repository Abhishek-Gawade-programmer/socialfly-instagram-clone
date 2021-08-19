from django.contrib import admin
from users.models import *
from posts.models import *
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Comment)
admin.site.register(ReportPost)
admin.site.register(PostActivity)
admin.site.register(UserActivity)
admin.site.register(Post,SimpleHistoryAdmin)
admin.site.register(PostImage)
admin.site.register(User,SimpleHistoryAdmin)
admin.site.register(SocialflyUser,SimpleHistoryAdmin)



