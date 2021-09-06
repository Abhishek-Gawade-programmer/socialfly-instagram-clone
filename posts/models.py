from users.models import User
from django.db import models
from django.utils.text import slugify
from  django.shortcuts import reverse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption =models.TextField( max_length=250,blank=True)
    tagged_people=models.ManyToManyField(User,related_name='tagged_people',blank=True)
    like_people=models.ManyToManyField(User,related_name='like_people',blank=True)
    bookmark_user=models.ManyToManyField(User,related_name='bookmark_user',blank=True)
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
        self.slug = slugify(self.caption[:100])+f'{self.id}-{self.user.username}'
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
    changed_by = models.ForeignKey(User,on_delete=models.CASCADE)
       
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post.caption +'::' +str(self.reason)+'::-->'+str(self.changed_by.username)
    
    def get_notification_verbose_title(self):
        map_titles={
            'tagged user':f'{self.post.user.username} Tagged you in post',
            'created new post':f'New Post By {self.post.user.username}',  
            'post report':f'Reported Your post {self.post.caption}',
            'like post':f'Like your post {self.post.caption}',
            'comment added':f'Commented On Your post {self.post.caption}',
        }

        return map_titles.get(self.reason)

    def get_notification_verbose_desrip(self):
        map_des={
            'tagged user':f'{self.post.user.username}Tagged you in post',
            'created new post':f'Have a look at {self.post.caption}',  
            'post report':f'Your post is Reported by {self.changed_by.username}',
            'like post':f'liked by {self.changed_by.username}',
            'comment added':f'Commented On Your post {self.post.caption}',
        }
        return map_des.get(self.reason)

    def save(self,*args,**kwargs):
        data={
            'title':self.get_notification_verbose_title(),
            'description':self.get_notification_verbose_desrip(),
            'user':False
            }
        if self.reason in ['post report','like post','comment added']:
            data['user']=self.post.user.username
        elif self.reason=="tagged user":
            data['user']=self.changed_by.username
        elif self.reason =="created new post":
            if self.post.user != changed_by.user:
                data['user']=self.post.user.username

        if data['user']:
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                    'global_notifcation_group',{
                        'command':'new_notification',
                        'type':'send_notification',
                        'value':data
                        }
                )
        
        super().save(*args,**kwargs)







































































