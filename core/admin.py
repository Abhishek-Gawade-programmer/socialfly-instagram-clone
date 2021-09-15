from django.contrib import admin
from users.models import *
from posts.models import *

admin.site.register(Comment)
admin.site.register(ReportPost)
admin.site.register(PostActivity)
admin.site.register(UserActivity)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(User)
admin.site.register(SocialflyUser)
admin.site.register(GenuineUser)



