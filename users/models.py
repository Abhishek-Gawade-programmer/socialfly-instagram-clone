from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.shortcuts import render,get_object_or_404,redirect
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('R', 'Rather Not To Say'),
)

class User(AbstractUser):
    is_genuine = models.BooleanField(default=False)

    @property
    def get_social_user(self):
        return  SocialflyUser.objects.get(user=self)


class SocialflyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    followers = models.ManyToManyField(User,related_name='followers',blank=True)
    following = models.ManyToManyField(User,related_name='following',blank=True)
    phone_number=models.CharField(max_length=20)
    bio=models.TextField(max_length=300,)
    birth_date=models.DateField(null=True,blank=True)
    profile_photo=models.ImageField(default='photo.jpeg',upload_to='profile_photo')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='R')
    is_private=models.BooleanField(default=False)
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def get_no_of_followers(self):
        return self.followers.all().count()

    def get_no_of_following(self):
        return self.following.all().count()

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'socialflyuser': self.pk})

    def get_user_post(self):
        from posts.models import Post
        return Post.objects.filter(user=self.user,posted=True)

    def get_user_bookmark(self):
        from posts.models import Post
        return Post.objects.filter(bookmark_user__in=[self.user])

    def allow_to_follow(self,socialflyuser):
        get_user = get_object_or_404(SocialflyUser, pk = socialflyuser)
        if get_user.user in self.followers.all():
            return False
        return True

    def __str__(self):
        return self.user.username +'----' +str(self.profile_photo)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class UserActivity(models.Model):
    reason=models.CharField(max_length=100)
    user_target=models.ForeignKey(User,on_delete=models.CASCADE,
        related_name='user_target')

    changed_by = models.ForeignKey(User,on_delete=models.CASCADE,
        related_name='changed_by',blank=True,null=True)

    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_target.username +'-' +str(self.reason)+'-->'