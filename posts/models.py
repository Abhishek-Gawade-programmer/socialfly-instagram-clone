from users.models import User
from django.db import models
from django.utils.text import slugify
from  django.shortcuts import reverse
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption =models.TextField( max_length=250,blank=True)
    tagged_people=models.ManyToManyField(User,related_name='tagged_people',blank=True)
    like_people=models.ManyToManyField(User,related_name='like_people',blank=True)
    posted=models.BooleanField(default=False)
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    slug=models.SlugField(max_length=100)


    def get_post_images(self):
        return PostImage.objects.filter(post=self)

    def get_post_comments(self):
        return Comment.objects.filter(post=self)

    def get_absolute_url(self):
        return reverse('posts:post_detail_view', kwargs={'slug': self.slug,'post_id':self.pk})

    def get_number_like(self):
        return self.like_people.all().count()

    def get_number_comments(self):
        return self.get_post_comments().count()
        
    def __str__(self):
        return self.user.username +'::' +str(self.caption)+'--'+self.slug

    class Meta:
        ordering = ('-created',)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.caption[:100])
        super().save(*args, **kwargs)


class PostImage(models.Model):
    image=models.ImageField(upload_to='user_photoes/')
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    def __str__(self):
    	return self.post.user.username +'::' +str(self.post.caption)


class Comment(models.Model):
    text =models.CharField( max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.post.user.username +'::' +str(self.text)

class ReportPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description =models.CharField( max_length=100,blank=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post.user.username +'::' +str(self.description)


class PostActivity(models.Model):
    reason=models.CharField(max_length=100)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User,on_delete=models.CASCADE,
        blank=True,null=True)
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.caption +'::' +str(self.reason)+'::-->'+str(self.changed_by.username)
    









































































