from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import messages

class User(AbstractUser):
    is_genuine = models.BooleanField(default=False)
    # def __str__(self):
    #     return  str(self.get_full_name())


class SocialflyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    followers = models.ManyToManyField(User,related_name='followers')
    following = models.ManyToManyField(User,related_name='following')
    phone_number=models.CharField(max_length=20)
    description=models.TextField(max_length=300)




    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)






from django.contrib.auth.signals import user_logged_out

def logout_notifier(sender, request, user, **kwargs):
	messages.info(request, f"{request.user.get_full_name()} Logout Successfully ")
   

user_logged_out.connect(logout_notifier)








