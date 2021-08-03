from django.db import models
from users.models import User


class Message(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	content=models.TextField(max_length=300,)
	timestamp =models.DateTimeField(auto_now_add=True)

	def last_10_meassges(self):
		return self.objects.order_by('-timestamp').all()[:10]

	def __str__(self):
  		return self.user.username +'----' +str(self.timestamp)[:10]


  		