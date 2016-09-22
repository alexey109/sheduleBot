#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import xlrd
import pandas as pd
import re
import datetime as dt
import string
import vk
import sys


timeFromLection = {
		1: '9:00-10:35',
		2: '10:45-12:20',
		3: '12:50-14:25',
		4: '14:35-16:10',
		5: '16:20-17:55',
		6: '18:00-21:20',
}

def dayFromRow(row_idx):
	return {
		      row_idx < 9: 0,		
		9  <= row_idx < 16: 1,
		16 <= row_idx < 21: 2,
		21 <= row_idx < 28: 3,
		28 <= row_idx < 34: 4,
		34 <= row_idx < 40: 5
	}[True]

def lectionFromTime(dt_time):
	return {
							dt_time < dt.time(9,0,0): 0,
		dt.time(9,0,0) 	 <= dt_time < dt.time(10,45,0): 1,
		dt.time(10,45,0) <= dt_time < dt.time(12,50,0): 2,
		dt.time(12,50,0) <= dt_time < dt.time(14,35,0): 3,
		dt.time(14,35,0) <= dt_time < dt.time(16,20,0): 4,
		dt.time(16,20,0) <= dt_time < dt.time(18,0,0): 5,
		dt.time(18,0,0) <= dt_time < dt.time(21,20,0): 6,
		dt.time(21,20,0) <= dt_time: 7
	}[True]

def isThatWeek(frequency, week_numb):
	week_numb = week_numb - dt.date(2016, 9, 1).isocalendar()[1] + 1
	
	if frequency == 'all':
		result = True
	elif 'I' in frequency:
		result = (week_numb % 2 == 0) == (frequency.strip() == 'II')
	else:
		result = str(week_numb) in re.split(r'[\s,]', frequency)
	
	return result

def getFrequency(cell_value):
	content = []
	frequencies = []

	for text in re.split(u'[\d\s,I]*\sн\.', cell_value):
		if text:
			content.append(re.sub(r'\n', ' ',text))

	found_frq = re.findall(u'[\d\s,I]*\sн\.', cell_value)
	for i, frequency in enumerate(found_frq):
		frequencies.append([content[i], re.sub(u'[\.\sн\n]', '',frequency)])

	if not found_frq:	
		frequencies = [[cell_value, 'all']]	

	return frequencies

def getClassroom(cell_value):
	if not cell_value:
		return ['-']
	return re.findall(u'[А-Яа-я]*-[\dА-Яа-я]*', cell_value)
	

def getLectionForGroup(group_name, day_of_week, week_numb, lection_start = 0):
	xls_sheet = xlrd.open_workbook("it-2k.-16_17-osen.xls").sheet_by_index(0)
	row_start = 4   # row when timetable start
	row_end   = 39  # row when timetable end

	group_colx = 0 
	while (xls_sheet.cell_value(rowx = 2, colx = group_colx) != group_name) and \
	(group_colx < xls_sheet.ncols) :
		group_colx += 1

	timetable  = ''
	for row_idx in range(row_start, row_end):
		text_cell_value = xls_sheet.cell_value(rowx = row_idx, colx = group_colx)
		day = dayFromRow(row_idx)
		if text_cell_value and day in day_of_week:
			lection_numb = xls_sheet.cell_value(rowx = row_idx, colx = 2)[0]
			classroom = getClassroom(xls_sheet.cell_value(rowx = row_idx, colx = group_colx+1))
			frequency = getFrequency(text_cell_value)
			for i, lection in enumerate(frequency):
				if isThatWeek(lection[1], week_numb) and int(lection_numb) >= int(lection_start):
					timetable += u'%.5s пара (%.5s, %.11s): %.100s\n' % \
					(lection_numb, classroom[i], timeFromLection[int(lection_numb)],lection[0].strip())
	
	return timetable


def getTommorowLections(group_name):
	day_of_week = [dt.datetime.today().weekday() + 1]
	week_numb = (dt.datetime.now() + dt.timedelta(days=1)).isocalendar()[1]
	
	return getLectionForGroup(group_name, day_of_week, week_numb)

def getAfterTommorowLections(group_name):
	day_of_week = [dt.datetime.today().weekday() + 2]
	week_numb = (dt.datetime.now() + dt.timedelta(days=2)).isocalendar()[1]
	
	return getLectionForGroup(group_name, day_of_week, week_numb)

def getTodayLections(group_name):
	day_of_week = [dt.datetime.today().weekday()]
	week_numb = dt.datetime.now().isocalendar()[1]
	
	return getLectionForGroup(group_name, day_of_week, week_numb)

def getNextLections(group_name):
	week_numb = dt.datetime.now().isocalendar()[1]
	lection_start = int(lectionFromTime(dt.datetime.now().time())) + 1
	if lection_start == 7:
		day_of_week = [dt.datetime.today().weekday()+1]
	else:
		day_of_week = [dt.datetime.today().weekday()]
	
	return getLectionForGroup(group_name, day_of_week, week_numb, lection_start)

def getLections(message):
	group_name = u'ИКБО-04-15'
	result = 'Error occured :('

	if u'следующие' in message:
		result = getNextLections(group_name)
	elif u'сегодня' in message:
		result = getTodayLections(group_name)
	elif u'завтра' in message:
		result = getTommorowLections(group_name)
	elif u'послезавтра' in message:
		result = getAfterTommorowLections(group_name)
	
	return result

if len(sys.argv) != 2:
  sys.exit("Not enough args")
message = str(sys.argv[1])
print getLections(message.decode('utf-8'))

#session = vk.Session()
#api = vk.API(session)
#print api.users.get(user_ids='385457066')
