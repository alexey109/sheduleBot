#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# tt = timetable

import xlrd
import pandas as pd
import re
import datetime as dt
import string

tt_native = xlrd.open_workbook("it-2k.-16_17-osen.xls").sheet_by_index(0)
	
def dayFromRow(row_idx):
	return {
		      row_idx < 9: u'Понедельник',		
		9  <= row_idx < 16: u'Вторник',
		16 <= row_idx < 21: u'Среда',
		21 <= row_idx < 28: u'Четверг',
		28 <= row_idx < 34: u'Пятница',
		34 <= row_idx < 40: u'Суббота'
	}[True]

def isThatWeek(frequency, date = dt.datetime.now()):
	week_numb = date.isocalendar()[1] - dt.date(2016, 9, 1).isocalendar()[1] + 1
	
	if 'I' in frequency:
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
		frequencies.append([content[i], re.sub(u'[\sн\n]', '',frequency)])

	if not found_frq:	
		frequencies = [[cell_value, 'all']]	

	return frequencies

def getClassroom(cell_value):
	if not cell_value:
		return ['']
	return re.findall(u'[А-Яа-яA-Za-z]*-\d*', cell_value)
	

def getLectionForGroup(group_name = u'ИКБО-04-15'):
	timetable  = ''
	group_colx = 0

	while (tt_native.cell_value(rowx = 2, colx = group_colx) != group_name) and \
	(group_colx < tt_native.ncols) :
		group_colx += 1

	for row_idx in range(4,39):
		text_cell_value = tt_native.cell_value(rowx = row_idx, colx = group_colx)
		if text_cell_value: 
			day = dayFromRow(row_idx)
			lection_numb = tt_native.cell_value(rowx = row_idx, colx = 2)[0]
			classroom = getClassroom(tt_native.cell_value(rowx = row_idx, colx = group_colx+1))
			frequency = getFrequency(text_cell_value)
			for i, lection in enumerate(frequency):
				print i, classroom
				timetable += u'day: %.20s, lection: %.5s, text: %.100s, classroom: %.5s, frequency: %.20s \n' % \
				(day, lection_numb, lection[0], classroom[i], lection[1])
	
	return timetable

print getLectionForGroup()

