#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# tt = timetable

import xlrd
import pandas as pd
import re
import datetime as dt


tt_native = xlrd.open_workbook("it-2k.-16_17-osen.xls").sheet_by_index(0)

# tt_group['day']['lection']= {'name': 'Философия', 'room': 'A-234', 'frequency': 1/2/3, 'dates': {1,3,5,7}}

group_colx = 0
while (tt_native.cell_value(rowx = 2, colx = group_colx) != u'ИКБО-04-15') and (group_colx < tt_native.ncols) :
	group_colx += 1

def isThatWeek(frequency):
	week_numb = dt.datetime.now().isocalendar()[1] - dt.date(2016, 9, 1).isocalendar()[1] + 1
	frequency = frequency.strip()
	if 'I' in frequency:
		result = (week_numb % 2 == 0) == (frequency == 'II')
	else:
		result = str(week_numb) in re.split(r'[\s,]', frequency)
	return result
	

day = u""
for row_idx in range(4,39):
	day_cell = tt_native.cell_value(rowx = row_idx, colx = 1).lower()
	day = day_cell if day_cell else day
	lection_numb = tt_native.cell_value(rowx = row_idx, colx = 2)[0]
	lection_freq = re.findall('^[\sI]*', tt_native.cell_value(rowx = row_idx, colx = group_colx))[0]
	lection_name = tt_native.cell_value(rowx = row_idx, colx = group_colx)
	classroom = tt_native.cell_value(rowx = row_idx, colx = group_colx+1)
	if lection_name: 
		print u'day: %.20s, lection: %.5s, text: %.100s, classroom: %.5s, frequency: %.20s \n' % \
			(day, lection_numb, lection_name, classroom, lection_freq)


	
	
