from django.db import models
from users.models import User
import uuid

class Room(models.Model):
	id=models.UUIDField(primary_key=True,
                    default=uuid.uuid4,
                    editable=False,
                    db_index=True,max_length=8)

	str_id= models.CharField(max_length=50,blank=True,null=True)
	user_eligible = models.ManyToManyField(User,)
	is_group=models.BooleanField(default=False)

	def last_message(self):
		if Message.objects.filter(room=self).exists():
			return Message.objects.filter(room=self).order_by('-timestamp')[0]
		else:
			return 'Start Chatting'

	def get_other_username(self,user):
		if not self.is_group:
			for group_member in self.get_user_set():
				if group_member !=user:
					return group_member

	def get_user_set(self):
		return set(self.user_eligible.all())

	def save(self, *args, **kwargs):
		self.str_id=self.id.hex
		super().save(*args, **kwargs)

class Message(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
	content=models.TextField(max_length=300,)
	room = models.ForeignKey(Room,on_delete=models.CASCADE)
	timestamp =models.DateTimeField(auto_now_add=True)
	def last_10_messages(room_str):
		return Message.objects.filter(
			room__str_id=room_str).order_by('-timestamp').all()[:10][::-1]

	def __str__(self):
  		return self.user.username +'----' +str(self.content)[:10]


class UserRoomInfo(models.Model):
	room = models.ForeignKey(Room,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	last_seen =models.DateTimeField(null=True,blank=True)

	def get_unseen_message(self):
		return Message.objects.filter(
				room=self.room,
				timestamp__gt=self.last_seen).count()

	def __str__(self):
  		return self.room.str_id +'----' +str(self.user.username)
