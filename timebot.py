#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# tt = timetable

import xlrd
import pandas as pd
import re


tt_native = xlrd.open_workbook("it-2k.-16_17-osen.xls").sheet_by_index(0)

# tt_group['day']['lection']= {'name': 'Философия', 'room': 'A-234', 'frequency': 1/2/3, 'dates': {1,3,5,7}}

group_colx = 0
while (tt_native.cell_value(rowx = 2, colx = group_colx) != u'ИКБО-04-15') and (group_colx < tt_native.ncols) :
	group_colx += 1

day = u""
for row_idx in range(4,39):
	day_cell = tt_native.cell_value(rowx = row_idx, colx = 1).lower()
	day = day_cell if day_cell else day
	lection_numb = tt_native.cell_value(rowx = row_idx, colx = 2)[0]
	lection_freq = re.match('[\s\d]*', tt_native.cell_value(rowx = row_idx, colx = group_colx)).groups()
	lection_name = tt_native.cell_value(rowx = row_idx, colx = group_colx) 
	print u'day: %.20s ,lection: %.5s ,text: %.100s ,frequency: %.20s' % \
		(day, lection_numb, lection_name, lection_freq)


	
	
