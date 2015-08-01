from django.db import models
from datetime import date

# Create your models here.
class Date(models.Model):
	class Meta():
		db_table = 'date'
	date = models.CharField(blank=False, 
							default=date.strftime(date.today(), format="%d%m%Y"), 
							primary_key=True, max_length=8)

class Event(models.Model):
	class Meta():
		db_table = 'event'
	event = models.CharField(max_length = 200)
	event_date = models.ForeignKey(Date)
