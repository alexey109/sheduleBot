#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import xlrd
import re
import datetime as dt


# This class present schedule, wich store like regural excel-file. 
# Now it can only show lection for special parameters, but in future
# it'll could load ecxel document into database and work with it,
# also new functions will be add like "when next lesson start" and etc.
class schedule:

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
		0: (4,9),
		1: (10,15),
		2: (16,21),
		3: (22,27),
		4: (28,33),
		5: (34,39)
	}

	# Open excel-document with scpecified group
	def openXlsForGroup(self, group_name):
		result = True
		try:
			if group_name[-1:] == '4':
				self.xls_sheet = xlrd.open_workbook("it-3k.-16_17-osen.xls").sheet_by_index(0)
			elif group_name[-1:] == '5':
				self.xls_sheet = xlrd.open_workbook("it-2k.-16_17-osen.xls").sheet_by_index(0)
			elif group_name[-1:] == '6':
				self.xls_sheet = xlrd.open_workbook("it-1k.-16_17-osen.xls").sheet_by_index(0)
			else:
				result = False
		except:
			result = False
		return result

	# Check if lection frequency match specified week number,
	# it mean that function returns true if lection have to be on that week.
	# Return type: boolean
	def isThatWeek(self, frequency, week_numb):
		week_numb = week_numb - dt.date(2016, 9, 1).isocalendar()[1] + 1
	
		if frequency == 'all':
			result = True
		elif 'I' in frequency:
			result = (week_numb % 2 == 0) == (frequency.strip() == 'II')
		elif '-' in frequency:
			period = re.split('-', frequency)
			result = (week_numb >= int(period[0])) and (week_numb <= int(period[1]))
		else:
			result = str(week_numb) in re.split(r'[\s,]', frequency)
	
		return result

	# Get frequency value from cell with lections name.
	# Return type: list of (lection_name, frequency)
	def getFrequency(self, cell_value):
		content = []
		frequencies = []

		for text in re.split(u'[\d\s,-I]*\sн\.', cell_value):
			if text:
				content.append(text)
			
		found_frq = re.findall(u'[\d\s,I-]*\sн\.', cell_value)
		for i, frequency in enumerate(found_frq):
			frequencies.append([content[i], re.sub(u'[\.\sн\n]', '',frequency)])

		if not found_frq:	
			frequencies = [[cell_value, 'all']]	

		return frequencies

	# Get classrooms values from cell with classroom
	# Return type: list of strings
	def getClassroom(self, cell_value):
		if not cell_value:
			return ['-']

		if u'база' in cell_value.lower():
			return [u'База']

		return re.findall(u'[А-Яа-я]*-[\d]*[А-Яа-я]*', cell_value)

	# Primary function, that returns lection timetable from timetable document for special parametrs.
	# Return type: string
	def getLectionForGroup(self, group_name, day_of_week, week_numb, lection_start = 0):
		row_start = self.rowFromDay[day_of_week][0]	
		row_end   = self.rowFromDay[day_of_week][1]

		if not self.openXlsForGroup(group_name):
			return ''
		group_colx = 0 
		while (group_colx < (self.xls_sheet.ncols - 1)) \
		and (self.xls_sheet.cell_value(rowx = 2, colx = group_colx) != group_name):
			group_colx += 1

		timetable  = ''
		for row_idx in range(row_start, row_end):
			text_cell_value = self.xls_sheet.cell_value(rowx = row_idx, colx = group_colx)
			if text_cell_value:
				lection_numb = self.xls_sheet.cell_value(rowx = row_idx, colx = 2)[0]
				classroom = self.getClassroom(self.xls_sheet.cell_value(rowx = row_idx, colx = group_colx+1))
				frequency = self.getFrequency(text_cell_value)
				for i, lection in enumerate(frequency):
					if self.isThatWeek(lection[1], week_numb) and int(lection_numb) >= int(lection_start):
						timetable += u'\n%.5s пара (%.5s, %.11s):\n%.100s\n' % \
						(lection_numb, classroom[i], self.timeFromLection[int(lection_numb)],lection[0].strip())
	
		return timetable if timetable else u'\nпар нет :)'

