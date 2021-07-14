from django import template
from django.utils import timezone

now = timezone.now()

register = template.Library()

@register.filter(name='date_str_output')
def date_friendly_output(object_note):
	current_time=timezone.now()


	if object_note.created == object_note.updated:
		differnce_between_times=current_time -object_note.created
	else:
		differnce_between_times=current_time -object_note.updated

	if int(differnce_between_times.seconds//60) < 2:
		return 'Recently '   
	elif int(differnce_between_times.seconds//60 )<59:
		return   str(int(differnce_between_times.seconds//60 ))+' min ago'


	elif int(differnce_between_times.days) == 0:
		return   str(int(differnce_between_times.seconds//3600 ))+' hrs ago'


	elif int(differnce_between_times.days) < 7:
		return   str(int(differnce_between_times.days))+' days ago'

	elif int(differnce_between_times.days) == 7:
		return   '1'+' week ago'


	elif int(differnce_between_times.days) >7:
		return   str(int(differnce_between_times.days//7))+' weeks ago'


	elif int(differnce_between_times.days) > 30:
		return   str(int(differnce_between_times.days//30))+' months ago'


	elif int(differnce_between_times.days) > 365:
		return   str(int(differnce_between_times.days//365))+' years ago'



