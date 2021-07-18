from users.models import User
from django.db import models
from simple_history.models import HistoricalRecords





class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    caption =models.CharField( max_length=100,blank=True)
    history = HistoricalRecords()
    video = models.FileField(upload_to='videos/',blank=True)
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username +'----' +str(self.caption)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PostImage(models.Model):
    image=models.ImageField()
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
    	return self.post.user.username +'----' +str(self.post.caption)





#  {'file[0]': [<InMemoryUploadedFile: Screenshot (7).png (image/png)>], 
#  'file[1]': [<InMemoryUploadedFile: Screenshot (6).png (image/png)>], 
# 'file[2]': [<InMemoryUploadedFile: Screenshot (5).png (image/png)>],
#  'file[3]': [<InMemoryUploadedFile: Screenshot (4).png (image/png)>],
#  'file[4]': [<InMemoryUploadedFile: Screenshot (3).png (image/png)>
# ]}


