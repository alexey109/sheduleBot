#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import xlrd
import re
import datetime as dt

import consts as ct


# This class present schedule, wich store like regural excel-file. 
# Now it can only show lection for special parameters, but in future
# it'll could load ecxel document into database and work with it,
# also new functions will be add like "when next lesson start" and etc.
class Schedule:
	
	# Return row number of start and end for a day of week in sheet
	# Return type: list of (start, end)
	rowFromDay = {
		0: (4,9),
		1: (10,15),
		2: (16,21),
		3: (22,27),
		4: (28,33),
		5: (34,39),
		6: (39,39) # TODO Fix this
	}

	# Open excel-document with scpecified group
	def openXlsForGroup(self, group_name):
		result = True
		try:
			self.xls_sheet = xlrd.open_workbook("it-2k.-16_17-osen.xls",  formatting_info=True).sheet_by_index(0)
			self.merged_cells = self.xls_sheet.merged_cells
		except:
			result = False
		return result

	# Get frequency value from cell with lections name.
	# Return type: list of (lection_name, frequency)
	def splitBody(self, text): 
		text = text.replace(u'н.', '') + '.' # Bag fix :(

		ST_BODY 	= 0
		ST_PARAMS	= 1
		ST_WEEK 	= 2

		teacher_kwd = [u'асс',u'доц',u'проф',u'ст.пр',u'преп',]

		rules = {
			ST_BODY: [
				{'expr': u'[А-Яа-я\./\s]', 'link': ST_BODY, 'ext': False, 'new_param': False},
				{'expr': '[0-9I]', 'link': ST_WEEK, 'ext': True, 'new_param': False},
				{'expr': '\(', 'link': ST_PARAMS, 'ext': False, 'new_param': True},
			],
			ST_PARAMS: [
				{'expr': '[^\)]', 'link': ST_PARAMS, 'ext': False, 'new_param': False},
				{'expr': '\)', 'link': ST_BODY, 'ext': False, 'new_param': False},
			],
			ST_WEEK: [
				{'expr': '[0-9I,\-\s]', 'link': ST_WEEK, 'ext': False, 'new_param': False},
				{'expr': '[^0-9I,\-\s]', 'link': ST_BODY, 'ext': False, 'new_param': False},
			]
		}

		status 	= ST_BODY
		i 		= 0
		body 	= {}
		params 	= []
		name = week = teacher = ''
		for idx, l in enumerate(text):
			for rule in rules[status]:
				if re.search(rule['expr'], l):
					status = rule['link']
					if (rule['ext'] and name) or (idx == len(text) - 1):
						for word in teacher_kwd:
							pos = name.find(word)
							if pos>0:
								teacher = name[pos:]
								name	= name[:pos]
								break

						body[i] = {}
						body[i]['name'] 	= name.strip()
						body[i]['teacher'] 	= teacher.strip()
						body[i]['params'] 	= params
						body[i]['week'] 	= week.strip()
						name = week = teacher = ''
						params = []
						i+=1
					if rule['new_param']:
						params.append('')
					break 						

			if l in ['(',')']:
				continue

			if status == ST_BODY:
				name += l
			elif status == ST_PARAMS:
				params[-1] += l
			elif status == ST_WEEK:
				week += l
		
		return body

	# Get classrooms values from cell with classroom
	# Return type: list of strings
	def getClassroom(self, cell_value):
		if not cell_value:
			return ['-']

		if u'база' in cell_value.lower():
			return [u'База']

		return re.findall(u'[А-Яа-я]*-[\d]*[А-Яа-я\-\d]*', cell_value)

	# Primary function, that returns lection timetable from timetable document for special parametrs.
	# Return type: string
	def getLections(self, group_name):
		if not self.openXlsForGroup(group_name):
			return []

		group_find	= False
		group_col 	= 0 
		group_row 	= 0
		group_name 	= group_name.lower()
		while (group_col < (self.xls_sheet.ncols - 1)) and (group_row < 5):
			if self.xls_sheet.cell_value(rowx = group_row, colx = group_col).lower() == group_name:
				group_find = True
				group_row += 2
				break

			group_col += 1
			if group_col == (self.xls_sheet.ncols - 1):
				group_row +=1	
				group_col = 0 

		if not group_find:
			raise Exception(ct.CONST.ERR_GROUP_NOT_FOUND)

		timetable  = []
		cell_number = 0
		for cell_row in range(group_row, group_row + 6*5):
			text_cell_value = self.xls_sheet.cell_value(rowx = cell_row, colx = group_col)
			cell_number += 1
			if text_cell_value:
				lection_numb = cell_number % 6
				day_numb = cell_number / 6
				classroom = self.getClassroom(self.xls_sheet.cell_value(rowx = cell_row, colx = group_col+1))
				body_splt = self.splitBody(text_cell_value)
				for idx in body_splt:
					try:
						room = classroom[idx]
					except:
						room = '-'
					
					# check parametr for lection number
					appended = False
					for i, param in enumerate(body_splt[idx]['params']):
						if (u'п' in param) and (not u'подгр' in param):
							for l in param:
								try:	
									lection = body_splt[idx].copy()
									lection.update({
										'day'	: day_numb,
										'numb'	: int(l),
										'room'	: room
									})
									timetable.append(lection)
									appended = True
								except:
									pass
					if appended:
						continue
						
					lection = body_splt[idx].copy()
					lection.update({
						'day'	: day_numb,
						'numb'	: lection_numb,
						'room'	: room
					})
					timetable.append(lection)

					for crange in self.merged_cells:			
						rlo, rhi, clo, chi = crange
   						if (cell_row == rlo) and (group_col == clo):
							for rowx in xrange(rlo+1, rhi):
								lection = body_splt[idx].copy()
								numb = rhi - cell_row
								lection.update({
									'day'	: day_numb,
									'numb'	: numb,
									'room'	: room
								})
								timetable.append(lection)
		return timetable


text = u'2,6,10,14 н. Э/Т лаб доц. Миленина С.А. I н. Физика лаб (2п)'
text2 = u'I н. Иностранный язык (4-5п) асс. Малина И.М. 4,8,12,16 н. Э/Т лаб доц. Матвеева Т.П.'
text3 = u'7,15 н. МРМ лаб (2-3п) (2 подгр)\
II н. Механика РМ лк (2п)\
3,11 н.МРМ лаб асс. Малина И.М. (2-3п) (1подгр)\
II н. Физика лк (3п) '
text4 = u'Физика лк'
parser = Schedule()

for subj in parser.getLections(u'ИВБО-07-15'):
	print "Day: %d, Numb: %d, Room: %s, Week: %s, Name: %s, Teacher: %s, Params: %s" % (
		subj['day'],		
		subj['numb'],		
		subj['room'],		
		subj['week'],		
		subj['name'],	
		subj['teacher'],
		str(subj['params']),					
	)

#res = parser.splitBody(text2)
#for i in res:
#	for el in res[i]:
#		print res[i][el]
#	print '--'

