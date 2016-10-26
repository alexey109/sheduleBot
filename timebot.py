#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime as dt
import time
import string
import vk
import sys
import re
from pymongo import MongoClient

import parser 
import consts as ct
import logger as lg
import security


# Class implement bot logic. The main idea of this bot to help everyone with schedule.
# Bot intergated to socialnet and like a friend can tell you what next lection you will have.
# Normal documentation will be in future.
class Timebot:
	def __init__(self):
		self.db = MongoClient().timebot
		self.logger = lg.Logger()

	# Check if lection frequency match specified week number,
	# it mean that function returns true if lection have to be on that week.
	# Return type: boolean
	def isThatWeek(self, native_week, base_week):
		base_week = base_week - dt.date(2016, 9, 1).isocalendar()[1] + 1
	
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

	def getLessons(self, group, day, week, lstart = 1, lfinish = 6):
		try:
			schedule = self.db.schedule.find({'group':group})[0]['schedule']
		except:
			raise Exception(ct.CONST.ERR_GROUP_NOT_FOUND)
		
		lessons = []
		for lesson in schedule:
			if (lesson['day'] == day) \
			and (self.isThatWeek(lesson['week'], week))\
			and (lesson['numb'] >= lstart)\
			and (lesson['numb'] <= lfinish):
				lessons.append((
					str(lesson['numb']),#TODO Remove to string 
					lesson['room'], 
					ct.CONST.LECTION_TIME[lesson['numb']],
					lesson['name']				
				))
		return lessons

	# Return lection number for specified time
	# Return type: integer
	def lectionFromTime(self, dt_time):
		return {
								dt_time < dt.time(9,0,0): 0,
			dt.time(9,0,0) 	 <= dt_time < dt.time(10,45,0): 1,
			dt.time(10,45,0) <= dt_time < dt.time(12,50,0): 2,
			dt.time(12,50,0) <= dt_time < dt.time(14,35,0): 3,
			dt.time(14,35,0) <= dt_time < dt.time(16,20,0): 4,
			dt.time(16,20,0) <= dt_time < dt.time(18,0,0):  5,
			dt.time(18,0,0)  <= dt_time < dt.time(21,20,0): 6,
			dt.time(21,20,0) <= dt_time: 7
		}[True]

	# Takes lection parametrs and put it message template
	# Return type: string
	def lFormat(self, params):
		if params == []:
			raise Exception(ct.CONST.ERR_NO_LECTIONS)

		result = ''
		for row in params:
			result += ct.CONST.UNI_TEMPLATE % (row)
		return result

	# Return tommorow 
	# Return type: string
	def getTommorow(self, group):
		day = (dt.datetime.today() + dt.timedelta(days=1)).weekday()
		week = (dt.datetime.now() + dt.timedelta(days=1)).isocalendar()[1]
		
		return self.lFormat(self.getLessons(group, day, week))

	# Return yesterday 
	# Return type: string
	def getYesterday(self, group):
		day = (dt.datetime.today() - dt.timedelta(days=1)).weekday()
		week = (dt.datetime.now() - dt.timedelta(days=1)).isocalendar()[1]

		return self.lFormat(self.getLessons(group, day, week))

	# Return after tommorow 
	# Return type: string
	def getAfterTommorow(self, group):
		day = (dt.datetime.today() + dt.timedelta(days=2)).weekday()
		week = (dt.datetime.now() + dt.timedelta(days=2)).isocalendar()[1]

		return self.lFormat(self.getLessons(group, day, week))

	# Return today 
	# Return type: string
	def getToday(self, group):
		day = dt.datetime.today().weekday()
		week = dt.datetime.now().isocalendar()[1]
	
		return self.lFormat(self.getLessons(group, day, week))

	# Return today next lection
	# Return type: string
	def getNext(self, group):
		week = dt.datetime.now().isocalendar()[1]
		lection_start = int(self.lectionFromTime(dt.datetime.now().time())) + 1
		if lection_start == 7:
			day = (dt.datetime.today() + dt.timedelta(days=1)).weekday()
		else:
			day = dt.datetime.today().weekday()
	
		return self.lFormat(self.getLessons(group, day, week,lection_start))

	# Return  for selected day
	# Return type: string
	def getByDay(self, group, day):
		week = dt.datetime.now().isocalendar()[1]
		if dt.datetime.today().weekday() >= day:
			week += 1
			
		return self.lFormat(self.getLessons(group, day, week))

	# Return current week number
	# Return type: string
	def getWeekNumb(self):
		week = dt.datetime.now().isocalendar()[1] - dt.date(2016, 9, 1).isocalendar()[1] + 1
		
		now = dt.datetime.now().date()
		start = dt.date(2016, 9, 1)
		end = dt.date(2016, 12, 26)
		delta = now - start
		amount = end - start
		percent = str(delta.days % amount.days) + '%'

		return (str(week), str(percent))

	# Return today 
	# Return type: string
	def getNowLection(self, group):
		day = dt.datetime.today().weekday()
		week = dt.datetime.now().isocalendar()[1]
		lection = int(self.lectionFromTime(dt.datetime.now().time()))
	
		return self.lFormat(self.getLessons(group, day, week, lection, lection))

	# Return  by number
	# Return type: string
	def getLectionByNumb(self, group, lection_in):
		day = dt.datetime.today().weekday()
		week = dt.datetime.now().isocalendar()[1]
		if lection_in in ct.CONST.NUMB_NAMES:
			lection = ct.CONST.NUMB_NAMES.index(lection_in)
		else:
			lection = int(lection_in[:-1])
	
		return self.lFormat(self.getLessons(group,day,week,lection,lection))

	# Return timing 
	# Return type: string
	def getLectionTime(self):
		msg = ''
		for i in ct.CONST.LECTION_TIME:
			msg += u'%s пара: %s\n' % (str(i), ct.CONST.LECTION_TIME[i])

		return msg

	def getTeacher(self, group):
		day	 = dt.datetime.today().weekday()
		week = dt.datetime.now().isocalendar()[1]
		numb = int(self.lectionFromTime(dt.datetime.now().time()))

		try:
			schedule = self.db.schedule.find({'group':group})[0]['schedule']
		except:
			raise Exception(ct.CONST.ERR_GROUP_NOT_FOUND)
		
		teacher = ''
		for lesson in schedule:
			if (lesson['day'] == day) \
			and (self.isThatWeek(lesson['week'], week))\
			and (lesson['numb'] == numb):
				teacher = lesson['teacher']
				if not teacher:
					raise Exception(ct.CONST.ERR_NO_TEACHER)

		if not teacher:
			raise Exception(ct.CONST.ERR_NO_LECTIONS)
		
		return teacher


	# Get group name from any string
	# Return type: string
	def getGroupFromString(self, string):
		match = re.search(u'[а-я]{4}[а-я]?-[0-9]{2}-[0-9]{2}', string)
		return match.group(0) if match else ''
		
	# Check is any word in text
	# Return type: boolean
	def wordsInTxt(self, words, text):
		result = {}
		for idx, word in enumerate(words):
			if word[:-1] in text:
				result = {'idx': idx, 'word': word}
				break
		return result

	def retriveBody(self, message):
		msg = message.copy()
		go_deeper = True
		while go_deeper:
			if self.is_exist(msg, 'fwd_messages'):
				msg = msg['fwd_messages'][0]
			else:
				go_deeper = False

		return msg['body']

	# Takes message and prepare answer for it.
	# Return type: string
	def getMyAnswer(self, message, is_chat):
		answer = ''
		title = message['title'].lower()
		text = self.retriveBody(message)
		text = text.lower()

		if is_chat and not any(re.match('^'+word, text) for word in ct.CONST.CHAT_KEYWORDS):
			raise Exception(ct.CONST.ERR_SKIP)

		group_from_title = self.getGroupFromString(title)
		group_from_msg = self.getGroupFromString(text)
		if group_from_msg:		
			group = group_from_msg
		elif group_from_title:
			group = group_from_title		
		elif is_chat:
			raise Exception(ct.CONST.ERR_NO_GROUP)

		if self.wordsInTxt(ct.CONST.CMD_KEYWORDS[ct.CONST.CMD_TO_DEVELOPER], text):
			try:
				user_id = str(message['uid'])
			except:
				user_id = ''
			self.logger.log(ct.CONST.LOG_FBACK, user_id + ' ' + text)
			answer = ct.CONST.USER_PREMESSAGE[ct.CONST.CMD_TO_DEVELOPER]
			return answer

		if not is_chat:
			try:
				group = self.db.users.find({'vk_id':message['uid']})[0]['group_name']
				if group_from_msg:
					group = group_from_msg
					self.db.users.update_one(
						{'vk_id':message['uid']},
						{'$set': {'group_name': group_from_msg}}
					)
					answer += ct.CONST.USER_PREMESSAGE[ct.CONST.SAVED_GROUP] % (group_from_msg)
			except:
				if group_from_msg:
					self.db.users.insert_one({'vk_id': message['uid'], 'group_name': group_from_msg})
					answer += ct.CONST.USER_PREMESSAGE[ct.CONST.SAVED_GROUP] % (group_from_msg)
				else:
					raise Exception(ct.CONST.ERR_NO_GROUP)	

		for command, keywords in ct.CONST.CMD_KEYWORDS.items():
			found_word = self.wordsInTxt(keywords, text)
			if found_word:	
				template = ct.CONST.USER_PREMESSAGE[command]

				if command == ct.CONST.CMD_POLITE:
					answer += ct.CONST.USER_PREMESSAGE[command]
				elif command == ct.CONST.CMD_NEXT:
					answer += template % (self.getNext(group))
				elif command == ct.CONST.CMD_TODAY:
					answer += template % (self.getToday(group))
				elif command == ct.CONST.CMD_AFTERTOMMOROW:
					answer += template % (self.getAfterTommorow(group))
				elif command == ct.CONST.CMD_YESTERDAY:
					answer += template % (self.getYesterday(group))
				elif command == ct.CONST.CMD_TOMMOROW:
					answer += template % (self.getTommorow(group))
				elif command == ct.CONST.CMD_WEEK:
					answer += template % self.getWeekNumb()
				elif command == ct.CONST.CMD_NOW:
					answer += template % (self.getNowLection(group))
				elif command == ct.CONST.CMD_LECTION_TIME:
					answer += template % (self.getLectionTime())
				elif command == ct.CONST.CMD_TEACHER:
					answer += template % (self.getTeacher(group))
				elif command == ct.CONST.CMD_DAY_OF_WEEK:
					answer += template % (found_word['word'], self.getByDay(group, found_word['idx']))
				elif command == ct.CONST.CMD_LECTION_NUMB:
					answer += template % (self.getLectionByNumb(group, found_word['word']))
				elif command == ct.CONST.CMD_HELP:
					answer += template
				else:
					self.logger.log(ct.CONST.LOG_MESGS, 'UNDEFINED: ' + text)
					raise Exception(ct.CONST.ERR_UNDEFINED)
				break
		if not answer:
			self.logger.log(ct.CONST.LOG_MESGS, 'UNDEFINED: ' + text)
			raise Exception(ct.CONST.ERR_SKIP)
		
		return answer
				
			

	# Open vkAPI session
	# Return type: vk.api object
	def openVkAPI(self):
		success = False
		while not success:
			try:
				self.logger.log(ct.CONST.LOG_WLOAD, 'Try to open new session.')
				session = vk.AuthSession(
					app_id = security.app_id, 
					user_login = security.user_login, 
					user_password = security.user_password, 
					scope = security.scope)
				api = vk.API(session)
				success = True
				self.logger.log(ct.CONST.LOG_WLOAD, 'New session opened.')
			except Exception as e:
				self.logger.log(ct.CONST.LOG_WLOAD, 'New session not opened!')
				self.logger.log(ct.CONST.LOG_ERROR, e)
				time.sleep(3)
		return api

	# Check element of tuple by index for existance
	# Return type: boolean
	def is_exist(self, tupl, index_name):
		try:
			tmp = tupl[index_name]
			result =  True
		except:
			result = False
		return result

	# Send answer for enter message
	# Return type: string 
	def sendMyAnswer(self, message):
		try:
			my_answer = ''
			is_chat = self.is_exist(message, 'chat_id')
			try:
				my_answer  = self.getMyAnswer(message, is_chat)
			except Exception, e:
				if isinstance(e.args[0], int):
					my_answer = ct.CONST.ERR_MESSAGES[e.args[0]]
				else:
					self.logger.log(ct.CONST.LOG_ERROR, e)
					return
			if my_answer: 
				if is_chat:
					self.api.messages.send(chat_id=message['chat_id'], message=my_answer)
				else:
					self.api.messages.send(user_id=message['uid'], message=my_answer)
				time.sleep(1)
		except Exception, e:
			self.logger.log(ct.CONST.LOG_WLOAD, 'Message not send!')
			self.logger.log(ct.CONST.LOG_ERROR, e)
			self.api = self.openVkAPI()

	# Scan enter messages and answer
	def run(self):		
		self.api = self.openVkAPI()
		while 1:
			time.sleep(1)
			try:
				new_messages = self.api.messages.get(out=0, count=5, time_offset=10)	
				del new_messages[0]
				for message in new_messages:
					if message['read_state'] == 0:
						self.sendMyAnswer(message)
			except Exception, e:
				self.logger.log(ct.CONST.LOG_ERROR, e)
				self.api = self.openVkAPI()


bot = Timebot()
bot.run()
