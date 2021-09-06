from django import template
from django.utils import timezone

now = timezone.now()

register = template.Library()

@register.filter(name='date_str_output')
def date_friendly_output(date_time):
	current_time=timezone.now()
	differnce_between_times=current_time-date_time

	if int(differnce_between_times.seconds//60) < 2:
		return 'NOW'   
	elif int(differnce_between_times.seconds//60 )<59:
		return   str(int(differnce_between_times.seconds//60 ))+' MINS AGO'


	elif int(differnce_between_times.days) == 0:
		return   str(int(differnce_between_times.seconds//3600 ))+' HRS AGO'


	elif int(differnce_between_times.days) < 7:
		return   str(int(differnce_between_times.days))+' DAYS AGO'

	elif int(differnce_between_times.days) == 7:
		return   '1'+' week ago'


	elif int(differnce_between_times.days) >7:
		return   str(int(differnce_between_times.days//7))+' WEEKS AGO'


	elif int(differnce_between_times.days) > 30:
		return   str(int(differnce_between_times.days//30))+' MONTHS AGO'


	elif int(differnce_between_times.days) > 365:
		return   str(int(differnce_between_times.days//365))+' YEARS AGO'



