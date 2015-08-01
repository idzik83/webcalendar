# -*- coding: utf-8 -*-
from django.shortcuts import render
from datetime import date, timedelta
from collections import OrderedDict
from models import Date, Event

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
	date_list = Date.objects.filter(date__endswith=cur_date.month + cur_date.year)
	date_index_list = []
	for date in date_list:
		date_index_list.append(date.date)
	calendar = month_calendar(date_index_list)
	return render(request, 'main.html', calendar)