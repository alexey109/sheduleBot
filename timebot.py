#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime as dt
import time
import string
import sys
import re
from operator import itemgetter
import hashlib
from random import randint

import consts as CONST
import logger as lg
import dbmodels as db


# The main idea of this bot to help everyone with schedule.
# Bot intergated to socialnet and like a friend can tell you what lection you will have.
# Normal documentation will be in future.
attachment	= ''
logger 		= lg.Logger()

def genBotID(any_string):
	md5_hash = hashlib.md5()
	id_free = False
	while not id_free:
		md5_hash.update(str(any_string) + 'e5cde62e4dc1c' + str(randint(0,10000)) )
		new_hash = md5_hash.hexdigest()
		try:
			user = db.Users.get(db.Users.bot_id == new_hash)
		except:
			user = False
		if not user:
			id_free = True
	return new_hash

def getLessonNumb(dt_time):
	return {
							dt_time < dt.time(9,0,0)  :	0,
		dt.time(8,0,0) 	 <= dt_time < dt.time(10,30,0): 1,
		dt.time(10,30,0) <= dt_time < dt.time(12,10,0): 2,
		dt.time(12,10,0) <= dt_time < dt.time(14,30,0): 3,
		dt.time(14,30,0) <= dt_time < dt.time(16,10,0): 4,
		dt.time(16,10,0) <= dt_time < dt.time(17,50,0): 5,
		dt.time(18,00,0) <= dt_time < dt.time(19,30,0): 6,
		dt.time(19,30,0) <= dt_time < dt.time(20
                                        ,00,0): 7,
		dt.time(20,00,0) <= dt_time < dt.time(21,40,0): 8,
		dt.time(21,40,0) <= dt_time					  :	9
	}[True]

def isWeeksEqual(native_week, base_week):
	base_week = base_week - dt.date(2017, 2, 6).isocalendar()[1] + 1

	if native_week == '':
		result = True
	elif 'I' in native_week:
		result = (base_week % 2 == 0) == (native_week.strip() == 'II')
	elif '-' in native_week:
		period = re.split('-', native_week)
		result = (base_week >= int(period[0])) and (base_week <= int(period[1]))
	else:
		result = str(base_week) in re.split(r'[\s,]', native_week)
	return result

def findFloor(room_native):
	room_native = room_native.lower().replace('-', '')
	campus 	= room_native[:1]
	room 	= room_native[1:]

	floor_found = {}
	if campus == u'а':
		for floor in CONST.MAP_DATA:
			if floor['nam_ru'][:1] == campus:
				for map_room in floor['rooms'].split(','):
					if room == map_room.replace(' ', ''):
						floor_found = floor
	else:
		for floor in CONST.MAP_DATA:
			if floor['nam_ru'] == (campus + room[:1]):
				floor_found = floor
	
	return floor_found

def getSchedule(params):
	schedule_base = db.Schedule.filter(group = params['group']['id'])
	try:
		db_user = db.Users.get(
			db.Users.vk_id == params['vk_id'], 
			db.Users.is_chat == params['is_chat']
		)
		schedule_user = db.UsersSchedule.filter(user = db_user)
	except:
		schedule_user = []
	schedule = []
	for event_base in schedule_base:
		no_major = True
		for event_user in schedule_user:
			if event_user.week == event_base.week \
			 and event_user.day == event_base.day \
			 and event_user.numb == event_base.numb:
			 	no_major = False
			 	break
		if not no_major:
			continue
		event = {
			'name'		: event_base.name,
			'week'		: event_base.week,
			'day'		: event_base.day,
			'numb'		: event_base.numb,
			'teacher'	: event_base.teacher,
			'room'		: event_base.room,
		}
		schedule.append(event)
	for event_user in schedule_user:
		if event_user.hide:
			continue
		event = {
			'name'		: event_user.name,
			'week'		: event_user.week,
			'day'		: event_user.day,
			'numb'		: event_user.numb,
			'teacher'	: event_user.teacher,
			'room'		: event_user.room,
		}
		schedule.append(event)
		
	if not schedule:
		raise Exception(CONST.ERR_NO_LECTIONS)
		
	schedule = sorted(schedule, key=itemgetter('day', 'numb'))
	return schedule

def getLessons(params, lstart = 1, lfinish = 8):
	schedule = getSchedule(params)
	
	lessons 	= []
	for event in schedule:
		if event['day'] == params['day'] and isWeeksEqual(event['week'], params['week'])	\
		and event['numb'] >= lstart	and event['numb'] <= lfinish:
		
			try:
				if params['find_first'] and lessons[-1]['day'] == event['day']:
					continue
			except:
				pass
				
			event['time'] = CONST.LECTION_TIME[event['numb']]
			lessons.append(event)
			day_buff = event['day']

	if not lessons:
		raise Exception(CONST.ERR_NO_LECTIONS)

	return lessons

def formatLessons(lesson_list):
	string = ''
	for lesson in lesson_list:
		string += CONST.USER_MESSAGE[CONST.CMD_UNIVERSAL].format(
			lesson['numb'],
			lesson['room'] + ', ' if lesson['room'] else '', 
			lesson['time'],
			lesson['name']				
		)

	return string	

def cmdUniversal(params):	
	if params['lnumb']:
		lnumb = params['lnumb']
		lesson_list = getLessons(params, lnumb, lnumb)
	else:
		lesson_list = getLessons(params)

	return formatLessons(lesson_list)

def cmdWeek(params):
	weeks = (params['date'].date() - dt.date(2017, 2, 5)).days / 7 + 1
	
	return CONST.USER_MESSAGE[CONST.CMD_WEEK].format(weeks)

def cmdLectionsTime(params):
	msg = ''
	for i in CONST.LECTION_TIME:
		msg += CONST.USER_MESSAGE[CONST.CMD_LECTIONS_TIME].format(i, CONST.LECTION_TIME[i])

	return msg

def cmdTeacher(params):
	lesson = getLessons(params, params['lnumb'], params['lnumb'])[0]
	teacher = lesson.get('teacher', '')
	if not teacher:
		raise Exception(CONST.ERR_NO_TEACHER)
	
	return teacher

def cmdHelp(params):
	return ''

def cmdPolite(params):
	return ''

def cmdFindLection(params):
	raise Exception(CONST.ERR_SKIP)
	return ''

def cmdFindTeacher(params):
	raise Exception(CONST.ERR_SKIP)
	return ''

def cmdWhenExams(params):
	week = params['week'] - dt.date(2017, 2, 6).isocalendar()[1] + 1

	now = dt.datetime.now().date()
	start = dt.date(2017, 2, 6)
	end = dt.date(2017, 5, 29)
	delta = end - now
	weeks = delta.days / 7
	days  = delta.days % 7

	delta = now - start
	amount = end - start
	percent = str(int(round((float(delta.days) / amount.days) * 100))) + '%'

	return CONST.USER_MESSAGE[CONST.CMD_WHEN_EXAMS].format(weeks, days, percent)

def cmdMap(params):
	global attachment

	floor = findFloor(params['keyword']['word'])

	if floor:
		attachment = 'photo385457066_' + floor['vk_id']
	else:
		raise Exception(CONST.ERR_NO_ROOM)

	return CONST.USER_MESSAGE[CONST.CMD_MAP].format(floor['desc'])

def cmdExams(params):
	#try:
	#	schedule = db.exams.find({'group':params['group']})[0]['schedule']
	#except:
	#	raise Exception(CONST.ERR_GROUP_NOT_FOUND)
	
	#events = ''
	#for event in schedule:
	#	if event['type'] == True:
	#		events += CONST.USER_MESSAGE[CONST.CMD_EXAMS].format(
	#			event['day'],
	#			event['time'],
	#			event['room'],
	#			event['name']
	#		)

	#return events
	return None

def cmdConsult(params):
	#try:
	#	schedule = db.exams.find({'group':params['group']})[0]['schedule']
	#except:
	#	raise Exception(CONST.ERR_GROUP_NOT_FOUND)
	
	#events = ''
	#for event in schedule:
	#	if event['type'] == False:
	#		events += CONST.USER_MESSAGE[CONST.CMD_CONSULT].format(
	#			event['day'],
	#			event['time'],
	#			event['room'],
	#			event['name']
	#		)

	#return events
	return None

def cmdSession(params):
	#global attachment
	
	#try:
	#	schedule = db.exams.find({'group':params['group']})[0]['schedule']
	#except:
	#	raise Exception(CONST.ERR_GROUP_NOT_FOUND)
	
	#events = ''
	#for event in schedule:
	#	type_name = u'Экзамен' if event['type'] else u'Консультация'		
	#	events += CONST.USER_MESSAGE[CONST.CMD_SESSION].format(
	#		event['day'],
	#		event['time'],
	#		event['room'],
	#		type_name,
	#		event['name']
	#	)
	#attachment = 'photo385457066_456239061'

	#return events
	return None

def cmdCalendarJn(params):
	global attachment	
	attachment = 'photo385457066_456239061'

	return ''

def cmdCalendarDc(params):
	global attachment
	attachment = 'photo385457066_456239062'

	return ''

def cmdZachet(params):
	#global attachment

	#try:
	#	schedule = db.zachet.find({'group':params['group']})[0]['schedule']
	#except:
	#	raise Exception(CONST.ERR_GROUP_NOT_FOUND)
	
	#events = ''
	#prev_day = 0
	#for event in schedule:
	#	if event['day'] < dt.datetime.today().day:
	#		continue
	#	if prev_day <> event['day']:
	#		events += '\n____________\n' + str(event['day']) + u' декабря:\n' 
	#	room =  '' if event['room'] == '-' else u', в ' + event['room']  	
	#	events += CONST.USER_MESSAGE[CONST.CMD_ZACHET].format(
	#		event['numb'],
	#		room,
	#		event['name']
	#	)
	#	prev_day = event['day']
	#attachment = 'photo385457066_456239062'

	#return events
	return None

def cmdMyGroup(params):

	return params['group']['code'].upper()

def cmdWhere(params):
	global attachment
			
	lesson_numb = ''
	if params['find_first']:
		lesson = getLessons(params)[0]
		lesson_numb = CONST.USER_MESSAGE[CONST.CMD_FIRST].format(lesson['numb'])
	else:
		lnumb = params['lnumb'] if params['lnumb'] else int(getLessonNumb(dt.datetime.now().time())) 
		lesson = getLessons(params, lnumb, lnumb)[0]
		
	if not lesson.get('room', False):
		raise Exception(CONST.ERR_NO_ROOM)

	text = CONST.USER_MESSAGE[CONST.CMD_WHERE].format(
		lesson['room'].upper(), 
		lesson['name'], 
		lesson_numb
	)

	floor = findFloor(lesson['room'])
	if floor:
		attachment = 'photo385457066_' + floor['vk_id']
	else:
		text += CONST.ERR_MESSAGES[CONST.ERR_NO_ROOM]
	
	return text
	
def cmdFor7days(params):
	day_amount = 7
	try:
		day_amount = int(re.search('[1-7]', params['keyword']['word']).group())
	except:
		pass
	
	text = ''
	for i in range(0, day_amount):	
		date = params['date'] + dt.timedelta(days = i)
		weekday = date.weekday()
		
		params['day'] 	= weekday
		params['week']	= date.isocalendar()[1]
		try:
			if params['lnumb']:
				lesson_list = getLessons(params, params['lnumb'], params['lnumb'])
			else:
				lesson_list = getLessons(params)
		except:
			continue

		if weekday == 6:
			continue
			
		if len(lesson_list) == 0:
			continue
			
		dname = CONST.DAY_NAMES[weekday].title()
		text += '_'*(len(dname) + len(dname)/2 + 6) + '\n' + dname + ' '+ date.strftime('%d.%m') + '\n'
		text += formatLessons(lesson_list)
		text += '\n'
		
	if len(text) == 0:
		raise Exception(CONST.ERR_NO_LECTIONS)
	
	return text
	
def cmdNewId(params):
	new_hash = genBotID(params['vk_id'])
	user = db.Users.get(
		db.Users.vk_id == params['vk_id'], 
		db.Users.is_chat == params['is_chat']
	)
	user.bot_id = new_hash
	user.save()
	return  CONST.USER_MESSAGE[CONST.CMD_NEW_ID].format(new_hash)
	
def cmdMyid(params):
	user = db.Users.get(
		db.Users.vk_id == params['vk_id'], 
		db.Users.is_chat == params['is_chat']
	)
	return  CONST.USER_MESSAGE[CONST.CMD_MYID].format(user.bot_id)
	
def cmdLink(params):
	return ''
	
def cmdSearchTeacher(params):
	split_teacher = params['keyword']['word'].replace(u'найди ', '').split(' ')
	teacher = split_teacher[0].title()
	like_string = split_teacher[0][:-1].title()
	initials = split_teacher[1] if len(split_teacher) >= 2 else ''
	initials += split_teacher[2] if len(split_teacher) >= 3 else ''
	initials = initials.replace('.', '')
	if initials:
		teacher += ' '
		like_string += '%'
		for l in initials:
			like_string += l.upper() + '%'
			teacher +=  l.upper() + '.'

	schedule = db.Schedule														\
		.select(
			db.Schedule.name,
			db.Schedule.teacher,
			db.Schedule.week,
			db.Schedule.day,
			db.Schedule.numb,
			db.Schedule.room,
			db.fn.COUNT(db.Schedule.room).alias('groups_amount')
		)																		\
		.where(db.Schedule.teacher.contains(like_string))						\
		.order_by(
			+db.Schedule.day,
			+db.Schedule.numb
        )																		\
		.group_by(
			db.Schedule.week,
			db.Schedule.day,
			db.Schedule.numb,
			db.Schedule.room,
			db.Schedule.name,
			db.Schedule.teacher,
		)																		\
		.dicts()

	delta_days = 0
	answer = ''
	answer_content = ''
	teachers = {}
	schedule = list(schedule)
	lessons_found = False
	while not answer_content and delta_days < 30:
		date = params['date'] + dt.timedelta(days = delta_days)
		delta_days += 1
		for event in schedule:
			if date.weekday() != event['day']									\
			or not isWeeksEqual(event['week'], date.isocalendar()[1]):
				continue

			if not answer_content:
				dname = CONST.DAY_NAMES_VINIT[date.weekday()]
				answer_content = u'Ближайшие пары в {} {}:\n\n'					\
					.format(dname, date.strftime('%d.%m') )

			name = event['name'][:20]
			name += '..' if len(event['name']) > 20 else ''
			answer_content += CONST.USER_MESSAGE[CONST.CMD_SEARCH_TEACHER]		\
				.format(
					event['numb'],
					event['room'],
					event['groups_amount'],
					name)

			teacher = event['teacher'].replace('\n', ' + ')
			try:
				teachers[teacher] += 1
			except:
				teachers[teacher] = 1
			lessons_found = True

	if len(teachers) > 1 and not initials:
		answer = u'Напишите инициалы, т.к. найдено несколько преподавателей:\n'
		answer += ', '.join(teachers)
	else:
		answer = answer_content
		answer += u'Преподаватель ' + max(teachers)

	if not lessons_found:
		raise Exception(CONST.ERR_NO_TEACHER_FOUND)

	return answer

def cmdMyTeachers(params):
	schedule_full = getSchedule(params)
	teachers_lessons = {}
	noteacher_counter = 0
	for event in schedule_full:
		if not event['teacher'] or len(event['teacher']) < 4:
			noteacher_counter += 1
			continue
		if teachers_lessons.get(event['teacher'], False):
			teachers_lessons[event['teacher']].append(event['name'])
		else:
			teachers_lessons[event['teacher']] = [event['name']]

	if not teachers_lessons:
		raise Exception(CONST.ERR_NO_TEACHER)

	answer = ''
	for teacher, lessons in teachers_lessons.items():
		lstr = '\n'.join(lessons)
		answer += CONST.USER_MESSAGE[CONST.CMD_MY_TEACHERS].format(teacher, lstr)

  	answer += CONST.USER_POSTMESSAGES[CONST.CMD_MY_TEACHERS] 					\
		.format(noteacher_counter)

	return answer


functions = {
	CONST.CMD_UNIVERSAL			: cmdUniversal,
	CONST.CMD_NEXT 				: cmdUniversal,
	CONST.CMD_TODAY 			: cmdUniversal,
	CONST.CMD_AFTERTOMMOROW 	: cmdUniversal,
	CONST.CMD_TOMMOROW			: cmdUniversal,
	CONST.CMD_YESTERDAY			: cmdUniversal,
	CONST.CMD_DAY_OF_WEEK 		: cmdUniversal,
	CONST.CMD_WEEK				: cmdWeek,
	CONST.CMD_NOW				: cmdUniversal,
	CONST.CMD_BY_DATE			: cmdUniversal,
	CONST.CMD_BY_TIME			: cmdUniversal,
	CONST.CMD_BY_NUMB			: cmdUniversal,
	CONST.CMD_HELP				: cmdHelp,
	CONST.CMD_POLITE			: cmdPolite,
	CONST.CMD_LECTIONS_TIME		: cmdLectionsTime,
	CONST.CMD_TEACHER			: cmdTeacher,
	CONST.CMD_FIND_LECTION		: cmdFindLection,
	CONST.CMD_WHEN_EXAMS		: cmdWhenExams,
	CONST.CMD_MAP				: cmdMap,
	CONST.CMD_EXAMS				: cmdExams,
	CONST.CMD_CONSULT			: cmdConsult,
	CONST.CMD_SESSION			: cmdSession,
	CONST.CMD_CALENDAR_JN		: cmdCalendarJn,
	CONST.CMD_CALENDAR_DC		: cmdCalendarDc,
	CONST.CMD_ZACHET			: cmdZachet,
	CONST.CMD_MYGROUP			: cmdMyGroup,
	CONST.CMD_WHERE				: cmdWhere,
	CONST.CMD_FOR7DAYS			: cmdFor7days,
	CONST.CMD_LECTIONS			: cmdUniversal,
	CONST.CMD_NEW_ID			: cmdNewId,
	CONST.CMD_MYID				: cmdMyid,
	CONST.CMD_LINK				: cmdLink,
	CONST.CMD_SEARCH_TEACHER	: cmdSearchTeacher,
	CONST.CMD_MY_TEACHERS		: cmdMyTeachers,
}

def findKeywords(words, text):
	keyword = {}
	for idx, word in enumerate(words):
		try:
			result = re.search(word, text).group()
		except:
			continue
		if result:
			keyword = {'idx': idx, 'word': result}
			break
	return keyword

def getGroup(params):
	answer 		= ''
	group_id 	= 0
	group_code 	= ''
	vk_id 		= params['chat_id'] if params['chat_id'] else params['user_id']
	try:
		db_user = db.Users.get(
			db.Users.vk_id == vk_id, 
			db.Users.is_chat == bool(params['chat_id'])
		)
		db_user.bot_activity =  dt.datetime.now()
		db_user.save()
	except:
		db_user = None

	match = re.search(u'[а-я]{4}[а-я]?-[0-9]{2}-[0-9]{2}', params['text'])
	msg_group = match.group(0) if match else ''
	params['text'] = params['text'].replace(msg_group, '')
	
	if msg_group and db_user:
		try:
			db_group = db.Groups.get(db.Groups.gcode == msg_group)
		except:
			raise Exception(CONST.ERR_GROUP_NOT_FOUND)		
		db_user.group = db_group.id
		db_user.save()
		
		group_id = db_user.group.id
		group_code = db_user.group.gcode
		
		answer += CONST.USER_PREMESSAGE[CONST.CMD_SAVE_GROUP].format(msg_group.upper())
	elif msg_group:
		try:
			db_group = db.Groups.get(db.Groups.gcode == msg_group)
		except:
			raise Exception(CONST.ERR_GROUP_NOT_FOUND)	
		db_user = db.Users(
			vk_id			= vk_id,
			is_chat			= bool(params['chat_id']),
			bot_id			= genBotID(vk_id),
			group			= db_group.id,
			notice_today	= False,
			notice_tommorow	= False,
			notice_week		= False,
			notice_map		= False,
			send_time		= None,
			notice_zerohour = None,
			bot_activity	= dt.datetime.now(),
		)
		db_user.save()

		group_id = db_user.group.id
		group_code = db_user.group.gcode

		answer += CONST.USER_PREMESSAGE[CONST.CMD_SAVE_GROUP].format(msg_group.upper())
		answer += CONST.USER_PREMESSAGE[CONST.CMD_HELP]
	elif db_user:
		group_id = db_user.group.id
		group_code = db_user.group.gcode
	else:
		raise Exception(CONST.ERR_NO_GROUP)

	group = {
		'id' 	: group_id,
		'code'	: group_code
	}
	return group, answer

# Apply hot functions
# 1 - today
# 2 - tomorrow
# 3 - week
# 4 - current on map
def applyHotFunc(command, markers):
	func_numb = command['keyword']['word']
	if func_numb == '1':
		command['code'] = CONST.CMD_UNIVERSAL
	if func_numb == '2':
		command['code'] = CONST.CMD_UNIVERSAL
		markers[CONST.CMD_TOMMOROW] = {'word': '', 'idx': ''}
	if func_numb == '3':
		command['code'] = CONST.CMD_FOR7DAYS
		command['keyword']['word'] = ''
	if func_numb == '4':
		command['code'] = CONST.CMD_WHERE
		
	return command, markers

def addZeroHourMsg(params):
	app_msg = ''
	db_user = db.Users.get(
		db.Users.vk_id == params['vk_id'], 
		db.Users.is_chat == params['is_chat']
	)
	current_wd = dt.datetime.now().weekday()
	try:
		if db_user.notice_zerohour.weekday() != current_wd:
			app_msg = CONST.MSG_ZERO_HOUR.format(CONST.DAY_NAMES[current_wd])
	except:
		pass
	db_user.notice_zerohour = dt.datetime.now()
	db_user.save()
	
	return app_msg

# Takes message and prepare answer for it.
# Return type: string
def analize(params):
	answer = ''
	answer_ok = False

	# Set default settings
	group, answer = getGroup(params)
	answer_ok = bool(answer)
	markers = {}
	default_kwd = {'word': u'сегодня', 'idx': 0}
	command	= {
		'code'	 : CONST.CMD_UNIVERSAL, 
		'keyword': default_kwd
	}
	date 	= dt.datetime.today()
	lesson 	= 0
	find_first	= False
	
	# Define command
	for cmd, keywords in CONST.KEYWORDS.items():
		if cmd in CONST.MARKERS:
			continue
		word = findKeywords(keywords, params['text']) 
		if word and (command['code'] >= cmd):
			command['code'] 	= cmd 
			command['keyword'] 	= word
			answer_ok 			= True
	if answer_ok:
		params['text'] = params['text'].replace(command['keyword']['word'], '')

	# Find all markers
	for cmd, keywords in CONST.KEYWORDS.items():
		if not cmd in CONST.MARKERS:
			continue
		word = findKeywords(keywords, params['text'])
		if word:
			params['text'] = params['text'].replace(word['word'], '')
			markers[cmd] = word

	if command['code'] == CONST.CMD_HOT_FUNC:
		command, markers = applyHotFunc(command, markers)

	if answer_ok and not markers:
		markers = {CONST.CMD_TODAY: default_kwd}

	# Apply markers for settings
	for cmd_code, keyword in markers.items():
		if cmd_code == CONST.CMD_TOMMOROW:
			date = dt.datetime.today() + dt.timedelta(days=1)
		elif cmd_code == CONST.CMD_NOW:
			lesson = int(getLessonNumb(dt.datetime.now().time()))
		elif cmd_code == CONST.CMD_NEXT:
			lesson = int(getLessonNumb(dt.datetime.now().time())) + 1
		elif cmd_code == CONST.CMD_AFTERTOMMOROW:
			date = dt.datetime.today() + dt.timedelta(days=2)
		elif cmd_code == CONST.CMD_YESTERDAY:
			date = dt.datetime.today() - dt.timedelta(days=1)
		elif cmd_code == CONST.CMD_DAY_OF_WEEK:
			keyword['word'] = CONST.DAY_NAMES_VINIT[keyword['idx']]
			for i in range(0,7):
				temp_date = dt.datetime.today() + dt.timedelta(days=i)
				if temp_date.weekday() == keyword['idx']:
					date = temp_date
					break
		elif cmd_code == CONST.CMD_BY_NUMB:
			lesson = keyword['idx']
			keyword['word'] = keyword['idx']
		elif cmd_code == CONST.CMD_BY_TIME:
			try:
				lesson = getLessonNumb(dt.datetime.strptime(keyword['word'], '%H:%M').time())
			except:
				del markers[cmd_code]
		elif cmd_code == CONST.CMD_BY_DATE:
			try:
				year = str(dt.date.today().year)
				date = dt.datetime.strptime(keyword['word']+year, '%d.%m%Y')
			except:
				try:
					day, month = keyword['word'].split(' ')
					mnumb = 0
					for idx, name in enumerate(CONST.MONTH_NAMES):
						if re.search(name, month):
							mnumb = idx + 1
							break
					date = dt.date(2017, mnumb, int(day))
				except:
					del markers[cmd_code]
		elif cmd_code == CONST.CMD_FIRST:
			find_first = True

	# Prepare parametrs for functions 
	cmd_params = {
		'vk_id'		: params['chat_id'] if params['chat_id'] else params['user_id'],
		'is_chat'	: bool(params['chat_id']),
		'group'		: group,
		'date'		: date,
		'day' 		: date.weekday(),
		'week'		: date.isocalendar()[1],
		'lnumb'		: lesson,
		'keyword'	: command['keyword'],
		'find_first': find_first
	}
		
	# Check markers after apply
	header = ''
	for cmd, kwd in markers.items():
		header += CONST.USER_PREMESSAGE[cmd].format(kwd['word'])
		answer_ok = True
	if not answer_ok:
		logger.log(CONST.LOG_MESGS, params['text'])
		raise Exception(CONST.ERR_SKIP)

	# Perform command and check for result
	answer += CONST.USER_PREMESSAGE[command['code']].format(markers = header)
	answer += functions[command['code']](cmd_params)
	
	if dt.datetime.now().hour < 2:
		answer += addZeroHourMsg(cmd_params)
	
	return answer	

def genAnswer(params):
	global attachment
	attachment = ''
	answer = {
		'text':'',
		'attachment':''
	}

	params['text']	= params['text'].lower()

	# Check for chat
	if params['chat_id'] and not any(re.match('^' + word, params['text']) for word in CONST.CHAT_KEYWORDS):
		raise Exception(CONST.ERR_SKIP)

	# Check feedback
	if any(re.search(word, params['text']) for word in CONST.FEEDBACK_KEYWORDS):
		logger.log(CONST.LOG_FBACK, str(params['user_id']) + ' ' + params['text'])
		answer['text'] = CONST.USER_PREMESSAGE[CONST.CMD_FEEDBACK]
		return answer
		
	answer['text'] = analize(params)
	answer['attachment'] = attachment
	
	return answer

def isNoticeTime():
	today = dt.datetime.now()
	return (today.hour >= CONST.NOTICE_START_TIME and today.hour <= CONST.NOTICE_END_TIME)
	
def saveNoticeTime(notice):
	try:
		user = db.Users.get(db.Users.vk_id == notice['user_id'], db.Users.is_chat == notice['is_chat'])
		user.send_time = dt.datetime.now()
		user.save()
	except:
		pass
	
def getNotice():
	today = dt.datetime.now()
	notice = {
		'user_id'		: '',
		'is_chat'		: '',
		'text'			: '',
		'attachment'	: '',
	}	
	
	user = None
	users = db.Users.select().where((
			db.Users.notice_today |
			db.Users.notice_tommorow |
			db.Users.notice_week |
			db.Users.notice_map
		), (
			(db.Users.send_time >> None) | 
			(db.Users.send_time < dt.datetime(today.year, today.month, today.day))
		)).limit(1)
	
	for u in users:
		user = u
		notice['user_id'] = user.vk_id
		notice['is_chat'] = user.is_chat
		break
	
	if not user:
		return notice
		
	params = {
		'user_id'	: user.vk_id,
		'chat_id'	: user.vk_id if user.is_chat else False,
		'text'		: ''
	}	
	def appendAnswer(notice, msg):
		try:
			params['text'] = msg
			answer = genAnswer(params)
			notice['text'] += '\n\n' + answer['text']
			notice['attachment'] += '\n' + answer['attachment']
		except:
			pass
		return notice
		
	if user.notice_today and today.weekday() != 6:
		notice = appendAnswer(notice, CONST.MSG_NOTICE_TODAY)
	if user.notice_tommorow and today.weekday() != 5:
		notice = appendAnswer(notice, CONST.MSG_NOTICE_TOMORROW)
	if user.notice_week and today.weekday() == 6:
		notice = appendAnswer(notice, CONST.MSG_NOTICE_WEEK)
	if user.notice_map and today.weekday() != 6:
		notice= appendAnswer(notice, CONST.MSG_NOTICE_MAP)
		
	if not (notice['text'] or notice['attachment']):
		saveNoticeTime(notice)
		raise Exception()
	
	return notice				

