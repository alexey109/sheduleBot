#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# tt = timetable

import xlrd
import pandas as pd
import re
import datetime as dt
import string

tt_native = xlrd.open_workbook("it-2k.-16_17-osen.xls").sheet_by_index(0)

group_colx = 0
while (tt_native.cell_value(rowx = 2, colx = group_colx) != u'ИВБО-04-15') and (group_colx < tt_native.ncols) :
	group_colx += 1
	
text = u'I н. Иностранный язык (4-5п)\
асс. Малина И.М.\
4,8,12,16 н. Э/Т лаб \
доц. Матвеева Т.П.\
II н. Иностранный язык (4-5п)\
асс. Малина И.М.'


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

	for text in re.split(u'[\d\s,I]*н\.', cell_value):
		if text:
			content.append(re.sub(u'\n', ' ',text))

	found_frq = re.findall(u'[\d\s,I]*н\.', cell_value)
	for i, frequency in enumerate(found_frq):
		frequencies.append([content[i], re.sub(u'[\sн\n]', '',frequency)])

	if not found_frq:	
		frequencies = [[cell_value, 'all']]	

	return frequencies


day = u""
for row_idx in range(4,39):
	text_cell_value = tt_native.cell_value(rowx = row_idx, colx = group_colx)
	if text_cell_value: 
		day_cell = tt_native.cell_value(rowx = row_idx, colx = 1).lower()
		day = day_cell if day_cell else day
		lection_numb = tt_native.cell_value(rowx = row_idx, colx = 2)[0]
		classroom = tt_native.cell_value(rowx = row_idx, colx = group_colx+1)
		frequency = getFrequency(text_cell_value)
		for lection in frequency:
			print u'day: %.20s, lection: %.5s, text: %.100s, classroom: %.5s, frequency: %.20s \n' % \
				(day, lection_numb, lection[0], classroom, lection[1])

