# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from datetime import date, timedelta
from collections import OrderedDict
from models import Date, Event
import json

class CalendarGenerator(object):
	def __init__(self, tuple_date):
		if type(tuple_date) is tuple:
			self.start_date, self.end_date = tuple_date
			self.curr_date = self.start_date

	def __iter__(self):
		return self

	def next(self):
		if self.curr_date >= self.end_date:
			raise StopIteration
		cur_date = self.curr_date
		self.curr_date += timedelta(1)
		return cur_date

def calendar_range(cur_date = date.today()):
	next_month = date(cur_date.year, cur_date.month+1, 1)
	first_month_day = date(cur_date.year, cur_date.month, 1)
	days_in_month = (next_month - first_month_day).days
	last_month_day = first_month_day + timedelta(days_in_month)
	days_in_calendar = 42
	first_monday = first_month_day - timedelta(first_month_day.weekday())
	last_sunday = first_monday + timedelta(days_in_calendar)
	return (first_monday, last_sunday)

def has_event(check_day_id, events_list):
	if check_day_id in events_list:
		return True
	return False

def define_class(check_day):
	if check_day.month != date.today().month:
		return 'not_cur_month'
	if check_day.weekday() >= 5:
		return 'weekend'
	return 'weekday'

def month_calendar(events_list, cur_date = date.today()):
	month_dict = {}
	month_dict['year'] = cur_date.year
	month_dict['month'] = cur_date.month
	month_dict['week_row'] = []
	cg = CalendarGenerator(calendar_range())
	for i in xrange(6):
		row = []
		for y in xrange(7):
			day = cg.next()
			day_detail = {}
			day_detail['id'] = str(day.day)+str(day.month)+str(day.year)
			day_detail['day'] = day.day
			day_detail['class'] = define_class(day)
			day_detail['has_event'] = has_event(day_detail['id'], events_list)
			# day_detail['is_weekend'] = is_weekend(day)
			row.append(day_detail)
		month_dict['week_row'].append(row)
	return month_dict

def index(request, cur_date = date.today()):
	date_idex = str(cur_date.month) + str(cur_date.year)
	date_list = Date.objects.filter(date__endswith=date_idex)
	date_index_list = []
	for date in date_list:
		date_index_list.append(date.date)
	calendar = month_calendar(date_index_list)
	return render(request, 'main.html', calendar)

def get_event_list(request):
	data = json.loads(request.body)
	try:
		date = Date.objects.get(date=data['date'])
		events_list = Event.objects.filter(event_date=date)
		events = []
		for event in events_list:
			curr_event = {}
			curr_event['event'] = event.event
			curr_event['event_id'] = event.id
			events.append(curr_event)
	except Date.DoesNotExist:
		return JsonResponse([], safe=False)
	return JsonResponse(events, safe=False)

def save_events(request):
	data = json.loads(request.body)
	data_success = {}
	for event in data['events']:
		event_id = event['id']
		if event_id == '':
			event_id = 0
		try:
			dateObject = Date.objects.get(date=data['date_event'])
			single_event = Event.objects.get(id=event_id)
		except Date.DoesNotExist:
			new_date = Date(date=data['date_event'])
			new_date.save()
			new_event = Event(event=event['event'], event_date=new_date)
			new_event.save()
		except Event.DoesNotExist:
			new_event = Event(event=event['event'], event_date=dateObject)
			new_event.save()
		else:
			single_event.event = event['event']
			single_event.save()
			data_success['Status'] = 'Success'
	return JsonResponse(data_success, safe=False)

def delete_event(request):
	data = json.loads(request.body)
	event_id = int(data['id'])
	event = Event.objects.get(id=event_id)
	event.delete()
	dateObject = Date.objects.get(date=data['date'])
	if not Event.objects.filter(event_date=dateObject).exists():
		dateObject.delete()
	return JsonResponse([], safe=False)
