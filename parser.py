#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import xlrd
import re
import datetime as dt

# This class present schedule, wich store like regural excel-file. 
# Now it can only show lection for special parameters, but in future
# it'll could load ecxel document into database and work with it,
# also new functions will be add like "when next lesson start" and etc.
class Parser:

	# Open excel-document with scpecified group
	def openDoc(self, doc_name):
		result = True
		try:
			self.sheet = xlrd.open_workbook(doc_name, formatting_info=True).sheet_by_index(0)
			self.merged_cells = self.sheet.merged_cells
		except:
			result = False
		return result

	# Get frequency value from cell with lections name.
	# Return type: list of (lection_name, frequency)
	def splitBody(self, text): 
		text = text.replace(u'\n', ' ')		
		text = text.replace(u'н.', '') + '.' # Bag fix :(

		ST_BODY 	= 0
		ST_PARAMS	= 1
		ST_WEEK 	= 2

		teacher_kwd = [u'асс',u'доц',u'проф',u'ст.', u'ст ',u'преп']

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

		return cell_value.split('\n')
		#return re.findall(u'[А-Яа-я]*-[\d]*[А-Яа-я\-\d]*', cell_value)

	# Primary function, that returns lection timetable from timetable document for special parametrs.
	# Return type: string
	def getGroupSchdl(self, group_row, group_col):
		timetable  = []
		cell_number = 0
		for cell_row in range(group_row, group_row + 6*6):
			text_cell_value = self.sheet.cell_value(rowx = cell_row, colx = group_col)
			if text_cell_value:
				lection_numb = cell_number % 6 + 1
				day_numb = cell_number / 6
				classroom = self.getClassroom(self.sheet.cell_value(rowx = cell_row, colx = group_col+1))
				body_splt = self.splitBody(text_cell_value)
				for idx in body_splt:
					try:
						if classroom[idx]:
							room = classroom[idx]
						elif body_splt.get(idx+1, 0):
							room = '-'
						else:
							room = classroom[idx+1]
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
					if lection['name']:
						timetable.append(lection)

					for crange in self.merged_cells:			
						rlo, rhi, clo, chi = crange
   						if (cell_row == rlo) and (group_col == clo):
							for rowx in xrange(rlo+1, rhi):
								lection = body_splt[idx].copy()
								numb = (rowx - group_row) % 6 + 1
								lection.update({
									'day'	: day_numb,
									'numb'	: numb,
									'room'	: room
								})
								if lection['name']:
									timetable.append(lection)
			cell_number += 1

		return timetable

	# type: true - exam, false - consult
	def getGroupExam(self, first_row, group_col):
		timetable  = []
		cell_row = first_row - 1
		while cell_row < 72:
			cell_row += 1
			ev_type = True	
			try:
				cell_type = self.sheet.cell_value(rowx = cell_row, colx = group_col).lower()
				if cell_type and ((u'консульт' in cell_type) or (u'экзамен' in cell_type)):
					if u'консульт' in cell_type:
						ev_type = False	
				else:
					continue

				cell_name = self.sheet.cell_value(rowx = cell_row+1, colx = group_col)
				cell_room = self.sheet.cell_value(rowx = cell_row, colx = group_col+2)	
				cell_time = self.sheet.cell_value(rowx = cell_row, colx = group_col+1) + 42139
				time = str(dt.datetime(*xlrd.xldate_as_tuple(cell_time, 0)).time())[:5]
				cell_day = self.sheet.cell_value(rowx = cell_row, colx = 2)[:2]
			except:
				continue

			
			event = {	
				'type'	: ev_type,
				'name'	: cell_name,
				'room'	: cell_room,
				'time'	: time,
				'day'	: str(int(cell_day))
			}	
			timetable.append(event)	

		return timetable

	# type: 'lections/exams'
	def getSchedule(self, document):
		if not self.openDoc(document):
			return {}

		schdl_type	= 'lections'
		group_col 	= 0 
		group_row 	= 0
		group_name 	= ''
		schedule 	= {}
		while (group_col < (self.sheet.ncols - 1)) and (group_row < 5):
			try: 
				group_name = self.sheet.cell_value(rowx = group_row, colx = group_col)
				if u'экзамен' in group_name.lower():
					exam = True
				match = re.search(u'[А-Яа-я]{4}[А-Яа-я]?-[0-9]{2}-[0-9]{2}', group_name)
			except:
				match = None
			if match:
				group_name = match.group(0).lower()
				try:
					if exam:
						schdl_type	= 'exams'
						schedule[group_name] = self.getGroupExam(group_row+1, group_col)
					else:
						schedule[group_name] = self.getGroupSchdl(group_row+2, group_col)
				except:
					pass

			group_col += 1
			if group_col == (self.sheet.ncols - 1):
				group_row +=1	
				group_col = 0 

		
		return schdl_type, schedule

