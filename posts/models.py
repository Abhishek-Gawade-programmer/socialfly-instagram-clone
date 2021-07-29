from users.models import User
from django.db import models
from simple_history.models import HistoricalRecords

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption =models.CharField( max_length=100,blank=True)
    history = HistoricalRecords()
    video = models.FileField(upload_to='videos/',blank=True)
    tagged_people=models.ManyToManyField(User,related_name='tagged_people',blank=True)
    like_people=models.ManyToManyField(User,related_name='like_people',blank=True)
    posted=models.BooleanField(default=False)
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def get_post_images(self):
        return PostImage.objects.filter(post=self)

    def get_absolute_url(self):
        return self.post.user.username +'::' +str(self.post.caption)

    def get_number_like(self):
        return self.like_people.all().count()
        
    def __str__(self):
        return self.user.username +'::' +str(self.caption)

    class Meta:
        ordering = ('-created',)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PostImage(models.Model):
    image=models.ImageField(upload_to='user_photoes/')
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    def __str__(self):
    	return self.post.user.username +'::' +str(self.post.caption)


class Comment(models.Model):
    text =models.CharField( max_length=100,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post.user.username +'::' +str(self.text)

class ReportPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description =models.CharField( max_length=100,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post.user.username +'::' +str(self.description)













































































