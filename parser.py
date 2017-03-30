#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openpyxl import load_workbook
import re
import datetime as dt

def saveGet(lst, idx, default):
	try:
		return lst[idx]
	except:
		return default

# This class present schedule, wich store like regural excel-file. 
# Now it can only show lection for special parameters, but in future
# it'll could load ecxel document into database and work with it,
# also new functions will be add like "when next lesson start" and etc.
class Parser:
	# Open excel-document with scpecified group
	def openDoc(self, doc_name):
		result = True
		try:
			self.wb = load_workbook(filename = doc_name)
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

	# Primary function, that returns lection timetable from timetable document for special parametrs.
	# Return type: string
	def getGroupSchdl(self, schedule, sheet):
	
		def isEventEqual(event1, event2):
			equal = False
			if event1['day'] == event2['day']	\
			and event1['numb'] == event2['numb']	\
			and event1['room'] == event2['room']	\
			and event1['name'] == event2['name']	\
			and event1['teacher'] == event2['teacher']:
				try:
					params = True
					for i in range(0, len(event1['params'])):
						if params and (event1['params'][i] != event2['params'][i]):
							params = False
				except:
					params = False
						
				if params and 'I' in event1['week'] and 'I' in event2['week']:
					equal = True
			return equal
			
		def checkFullDay(name):
			keywords = [u'воен', u'производств.*практ', u'день.*самост']
			find = False
			for keyword in keywords:
				if re.search(keyword, name.lower()):
					find = True
					break
			return find
	
		for row in sheet.iter_rows(min_row=2, max_col=sheet.max_column, max_row=2):
			for cell in row:
				lector_flag = False
				if not cell.internal_value:
					continue
				try:
					match = re.search(u'[А-Яа-я]{4}[А-Яа-я]?-[0-9]{2}-[0-9]{2}', cell.internal_value)
					if not match:
						continue
				except:
					continue
				j = cell.col_idx
				group = cell.internal_value.lower()
				lections = []
				maybe_room	= sheet.cell(row = 3, column = j + 3).internal_value
				if maybe_room and (u'ауд' in maybe_room):
					lector_flag = True
				
				for i in range(4, 76):
					content = sheet.cell(row = i, column = j).internal_value
					if not content:
						continue
					etype = sheet.cell(row = i, column = j+1).internal_value
					etype = etype.split('\n') if etype else ''
					if lector_flag:
						lector	= sheet.cell(row = i, column = j+2).internal_value
						rooms 	= sheet.cell(row = i, column = j+3).internal_value
					else:
						lector	= ''
						rooms 	= sheet.cell(row = i, column = j+2).internal_value
					rooms = rooms.split('\n') if rooms else []
					
					cell_day  = (i-4)/12
					cell_numb = (i - cell_day*12)/2 - 1
					cell_week = 'I' if (i - cell_day*12)%2 == 0 else 'II' 
					info = self.splitBody(content)						
					for i in range(0, len(info)):
						event_type = saveGet(etype, i, '')
						room = saveGet(rooms, i, '-')
						
						if len(info[i]['name']) < 2:
							continue
						event = {
							'day'	: cell_day,
							'numb'	: cell_numb,
							'room'	: room,
							'week'	: info[i]['week'] if info[i]['week'] else cell_week,
							'name'	: info[i]['name'] + ' ' + event_type,
							'teacher':lector,
							'params': info[i]['params']
						}
						
						append_flag = True
						for l in lections:
							if isEventEqual(l, event):
								l['week'] = ''
								append_flag = False
						
						if append_flag:
							if checkFullDay(event['name']):
								event['week'] = ''
								event['numb'] = 1
							lections.append(event)
						
				
				schedule[group] = lections
		
		return schedule

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

	def getGroupZachet(self, group_row, group_col):
		timetable  = []
		cell_number = 0
		for cell_row in range(group_row, group_row + 6*6):
			cell_txt = self.sheet.cell_value(rowx = cell_row, colx = group_col)
			if cell_txt:
				lection_numb = cell_number % 6 + 1
				classroom = self.getClassroom(self.sheet.cell_value(rowx = cell_row, colx = group_col+1))
				room = '-'
				for r in classroom:
					if r:
						room = r
						break

				dates = re.findall('\d\d.\d\d.\d\d', cell_txt)

				for d in dates:
					cell_txt = cell_txt.replace(d, '')

				name = ''
				for l in cell_txt:
					if re.search(u'[А-Яа-я\.\d\(\)\s]', l):
						name += l

				name = name.replace('\n','').strip()			

				for d in dates:
					event = {
						'day'	: int(d[:2]),
						'name'	: name,
						'room'	: room,
						'numb'	: lection_numb				
					}
					timetable.append(event)

			cell_number += 1

		timetable.sort(key=lambda t:t['day'])
		return timetable


	# type: 'lections/exams/zachet'
	def getSchedule(self, document):
		if not self.openDoc(document):
			return {}

		schedule 	= {}
		for sheet in self.wb:
			schdl_type	= 'lections'
			exam		= False
			zachet		= False
			group_name 	= ''
		
			for row in sheet.iter_rows(min_row=1, max_col=sheet.max_column, max_row=3):
				for cell in row:
					try: 
						group_name = cell.internal_value
						if u'экзамен' in group_name.lower():
							exam = True
						elif u'зачет' in group_name.lower():
							zachet = True
					except:
						match = None
						
			if exam:
				schdl_type	= 'exams'
				schedule[group_name] = self.getGroupExam(group_row+2, group_col)
			elif zachet:
				schdl_type	= 'zachet'
				schedule[group_name] = self.getGroupZachet(group_row+2, group_col)
			else:
				schedule = self.getGroupSchdl(schedule, sheet)
		
		return schdl_type, schedule

