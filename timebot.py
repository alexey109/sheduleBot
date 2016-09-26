#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import xlrd
import re
import datetime as dt
import time
import string
import vk
import sys
from random import randint

# Dictionary of lections start-end time
# Return type: string
timeFromLection = {
	1: '9:00-10:35',
	2: '10:45-12:20',
	3: '12:50-14:25',
	4: '14:35-16:10',
	5: '16:20-17:55',
	6: '18:00-21:20',
}

# Return row number of start and end for a day of week in sheet
# Return type: list of (start, end)
rowFromDay = {
	0: (4,8),
	1: (9,15),
	2: (16,20),
	3: (21,27),
	4: (28,33),
	5: (34,39)
}

# Return lection number for specified time
# Result type: integer
def lectionFromTime(dt_time):
	return {
							dt_time < dt.time(9,0,0): 0,
		dt.time(9,0,0) 	 <= dt_time < dt.time(10,45,0): 1,
		dt.time(10,45,0) <= dt_time < dt.time(12,50,0): 2,
		dt.time(12,50,0) <= dt_time < dt.time(14,35,0): 3,
		dt.time(14,35,0) <= dt_time < dt.time(16,20,0): 4,
		dt.time(16,20,0) <= dt_time < dt.time(18,0,0): 5,
		dt.time(18,0,0)  <= dt_time < dt.time(21,20,0): 6,
		dt.time(21,20,0) <= dt_time: 7
	}[True]

# Check if lection frequency match specified week number,
# it mean that function returns true if lection have to be on that week.
# Result type: boolean
def isThatWeek(frequency, week_numb):
	week_numb = week_numb - dt.date(2016, 9, 1).isocalendar()[1] + 1
	
	if frequency == 'all':
		result = True
	elif 'I' in frequency:
		result = (week_numb % 2 == 0) == (frequency.strip() == 'II')
	else:
		result = str(week_numb) in re.split(r'[\s,]', frequency)
	
	return result

# Get frequency value from cell with lections name.
# Result type: list of (lection_name, frequency)
def getFrequency(cell_value):
	content = []
	frequencies = []

	for text in re.split(u'[\d\s,I]*\sн\.', cell_value):
		if text:
			content.append(text)

	found_frq = re.findall(u'[\d\s,I]*\sн\.', cell_value)
	for i, frequency in enumerate(found_frq):
		frequencies.append([content[i], re.sub(u'[\.\sн\n]', '',frequency)])

	if not found_frq:	
		frequencies = [[cell_value, 'all']]	

	return frequencies

# Get classrooms values from cell with classroom
# Result type: list of strings
def getClassroom(cell_value):
	if not cell_value:
		return ['-']
	return re.findall(u'[А-Яа-я]*-[\dА-Яа-я]*', cell_value)
	

# Primary function, that returns lection timetable from timetable document for special parametrs.
# Result type: string
def getLectionForGroup(group_name, day_of_week, week_numb, lection_start = 0):
	xls_sheet = xlrd.open_workbook("it-2k.-16_17-osen.xls").sheet_by_index(0)
	row_start = rowFromDay[day_of_week][0]	
	row_end   = rowFromDay[day_of_week][1]

	group_colx = 0 
	while (xls_sheet.cell_value(rowx = 2, colx = group_colx) != group_name) and \
	(group_colx < xls_sheet.ncols) :
		group_colx += 1

	timetable  = ''
	for row_idx in range(row_start, row_end):
		text_cell_value = xls_sheet.cell_value(rowx = row_idx, colx = group_colx)
		if text_cell_value:
			lection_numb = xls_sheet.cell_value(rowx = row_idx, colx = 2)[0]
			classroom = getClassroom(xls_sheet.cell_value(rowx = row_idx, colx = group_colx+1))
			frequency = getFrequency(text_cell_value)
			for i, lection in enumerate(frequency):
				if isThatWeek(lection[1], week_numb) and int(lection_numb) >= int(lection_start):
					timetable += u'\n%.5s пара (%.5s, %.11s):\n %.100s\n' % \
					(lection_numb, classroom[i], timeFromLection[int(lection_numb)],lection[0].strip())
	
	return timetable


# Return tommorow lections
# Result type: string
def getTommorowLections(group_name):
	day_of_week = (dt.datetime.today() +  + dt.timedelta(days=1)).weekday()
	week_numb = (dt.datetime.now() + dt.timedelta(days=1)).isocalendar()[1]

	return getLectionForGroup(group_name, day_of_week, week_numb)

# Return after tommorow lections
# Result type: string
def getAfterTommorowLections(group_name):
	day_of_week = (dt.datetime.today() + dt.timedelta(days=2)).weekday()
	week_numb = (dt.datetime.now() + dt.timedelta(days=2)).isocalendar()[1]
	return getLectionForGroup(group_name, day_of_week, week_numb)

# Return today lections
# Result type: string
def getTodayLections(group_name):
	day_of_week = dt.datetime.today().weekday()
	week_numb = dt.datetime.now().isocalendar()[1]
	
	return getLectionForGroup(group_name, day_of_week, week_numb)

# Return today next lection
# Result type: string
def getNextLections(group_name):
	week_numb = dt.datetime.now().isocalendar()[1]
	lection_start = int(lectionFromTime(dt.datetime.now().time())) + 1
	if lection_start == 7:
		day_of_week = (dt.datetime.today() +  + dt.timedelta(days=1)).weekday()
	else:
		day_of_week = dt.datetime.today().weekday()
	
	return getLectionForGroup(group_name, day_of_week, week_numb, lection_start)

def getLections(message):
	group_name = u'ИКБО-04-15'
	result = ''

	if not((u'пары' in message) or (u'лекции' in message)):
		return result
	if u'дальше' in message:
		result = u'Следующие пары:\n\n' + getNextLections(group_name)
	elif u'сегодня' in message:
		result = u'Пары сегодня:\n\n' + getTodayLections(group_name)
	elif u'послезавтра' in message:
		result = u'Пары послезавтра:\n\n' + getAfterTommorowLections(group_name)
	elif u'завтра' in message:
		result = u'Пары завтра:\n\n' + getTommorowLections(group_name)
	
	return result

''' For debugging.
if len(sys.argv) != 2:
	sys.exit("Not enough args")
message = str(sys.argv[1])
print getLections(message.decode('utf-8'))
'''
 
# Open vkAPI session
success = False
while not success:
	try:
		session = vk.AuthSession(app_id='5637421', user_login='+79296021208', user_password='timebot109', scope='4096')
		api = vk.API(session)
		success = True
	except:
		time.sleep(10)

# Scan enter messages and answer
counter = 0
while counter < 3600*24*4:
	counter += 1
	try:
		response = api.messages.get(out=0, count=10, time_offset=20)
	except:
		response = []	
	for message in response:
		try:
			if message['read_state'] == 0: 
				lections = getLections(message['body'].lower())
				if lections:
					try:
						api.messages.send(chat_id=message['chat_id'], message=lections)
					except:
						api.messages.send(user_id=message['uid'], message=lections)
					time.sleep(1)
		except:
			time.sleep(1)

