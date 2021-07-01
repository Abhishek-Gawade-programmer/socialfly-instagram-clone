from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('R', 'Rather Not To Say'),
)




class User(AbstractUser):
    is_genuine = models.BooleanField(default=False)
    # def __str__(self):
    #     return  str(self.get_full_name())


class SocialflyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    followers = models.ManyToManyField(User,related_name='followers',blank=True)
    following = models.ManyToManyField(User,related_name='following',blank=True)
    phone_number=models.CharField(max_length=20)
    bio=models.TextField(max_length=300,)
    birth_date=models.DateField(null=True,blank=True)
    profile_photo=models.ImageField(default='photo.jpeg',upload_to='profile_photo')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='R')
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def get_no_of_followers(self):
        return self.followers.all().count()

    def get_no_of_following(self):
        return self.following.all().count()
    

    def __str__(self):
        return self.user.username
    


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)







