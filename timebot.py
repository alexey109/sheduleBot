#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime as dt
import time
import string
import vk
import sys

import parser 


# Class implement bot logic. The main idea of this bot to help everyone with schedule.
# Bot intergated to socialnet and like a friend can tell you what next lection you will have.
# Normal documentation will be in future.
class timebot():
	# Russian day names in dative.
	__day_names=(
		u'понедельник', 
		u'вторник',
		u'среду',
		u'четверг',
		u'пятницу',
		u'субботу'
	)
	
	def __init__(self):
		self.api = self.openVkAPI()
		self.schedule = parser.schedule()

	# Return lection number for specified time
	# Return type: integer
	def lectionFromTime(self, dt_time):
		return {
								dt_time < dt.time(9,0,0): 0,
			dt.time(9,0,0) 	 <= dt_time < dt.time(10,45,0): 1,
			dt.time(10,45,0) <= dt_time < dt.time(12,50,0): 2,
			dt.time(12,50,0) <= dt_time < dt.time(14,35,0): 3,
			dt.time(14,35,0) <= dt_time < dt.time(16,20,0): 4,
			dt.time(16,20,0) <= dt_time < dt.time(18,0,0): 5,
			dt.time(18,0,0)  <= dt_time < dt.time(21,20,0): 6,
			dt.time(21,20,0) <= dt_time: 7
		}[True]

	# Return tommorow lections
	# Return type: string
	def getTommorowLections(self, group_name):
		day_numb = (dt.datetime.today() + dt.timedelta(days=1)).weekday()
		week_numb = (dt.datetime.now() + dt.timedelta(days=1)).isocalendar()[1]

		message = u'Пары завтра:\n\n'
		message += self.schedule.getLectionForGroup(group_name, day_numb, week_numb)
		return message

	# Return after tommorow lections
	# Return type: string
	def getAfterTommorowLections(self, group_name):
		day_numb = (dt.datetime.today() + dt.timedelta(days=2)).weekday()
		week_numb = (dt.datetime.now() + dt.timedelta(days=2)).isocalendar()[1]
		message = u'Пары послезавтра:\n\n'
		message += self.schedule.getLectionForGroup(group_name, day_numb, week_numb)
		return message

	# Return today lections
	# Return type: string
	def getTodayLections(self, group_name):
		day_numb = dt.datetime.today().weekday()
		week_numb = dt.datetime.now().isocalendar()[1]
	
		message = u'Пары сегодня:\n\n'
		message += self.schedule.getLectionForGroup(group_name, day_numb, week_numb)
		return message

	# Return today next lection
	# Return type: string
	def getNextLections(self, group_name):
		week_numb = dt.datetime.now().isocalendar()[1]
		lection_start = int(self.lectionFromTime(dt.datetime.now().time())) + 1
		if lection_start == 7:
			day_numb = (dt.datetime.today() + dt.timedelta(days=1)).weekday()
		else:
			day_numb = dt.datetime.today().weekday()
	
		message = u'Следующие пары:\n\n'
		message += self.schedule.getLectionForGroup(group_name, day_numb, week_numb, lection_start)
		return message

	# Return lections for selected day
	# Return type: string
	def getLectionsByDay(self, group_name, day_numb):
		week_numb = dt.datetime.now().isocalendar()[1]
		if dt.datetime.today().weekday() >= day_numb:
			week_numb += 1
			
		message = u'Пары в '+ self.__day_names[day_numb] + ':\n\n'
		message += self.schedule.getLectionForGroup(group_name, day_numb, week_numb)
		return message

	# Retrun message that bot send back to user.
	# Return type: string
	def getLections(self, message):
		group_name = u'ИКБО-04-15'
		answer = ''

		if any(word in message for word in (u'пары', u'лекции')):
			return answer

		if	 u'сегодня' in message:
			answer = self.getTodayLections(group_name)
		elif u'послезавтра' in message:
			answer = self.getAfterTommorowLections(group_name)
		elif u'завтра' in message:
			answer = self.getTommorowLections(group_name)
		elif any(word in message for word in (u'дальше', u'следующие')):
			answer = self.getNextLections(group_name)
		else:
			for day_idx, day_name in enumerate(self.__day_names):
				if day_name in message:
					answer = self.getLectionsByDay(group_name, day_idx)
			
	
		return answer

	# Check element of tuple by index for existance
	# Return type: boolean
	def is_exist(self, tupl, index_name):
		try:
			tmp = tupl[index_name]
			result =  True
		except:
			result = False
		return result

	# Open vkAPI session
	# Return type: vk.api object
	def openVkAPI(self):
		success = False
		while not success:
			try:
				print 'Try to open new session.'
				session = vk.AuthSession(
					app_id='5637421', 
					user_login='+79296021208', 
					user_password='timebot109', 
					scope='4096')
				api = vk.API(session)
				success = True
				print 'New session opened.'
			except:
				print 'Error ocured when tried to open session!'
				time.sleep(4)
		return api

	# Send answer for enter message
	# Return type: string 
	# TODO Add status code, or use boolean.
	def sendAnswer(self, message):
		print 'Got new message ' + str(dt.datetime.now()) 
		result = ''

		try:
			answer = self.getLections(message['body'].lower())
			if answer: 
				if self.is_exist(message, 'chat_id'):
					self.api.messages.send(chat_id=message['chat_id'], message=answer)
				else:
					self.api.messages.send(user_id=message['uid'], message=answer)
				result = 'Message send.'
		except Exception, e:
			result = 'Message not send: \n' + str(e)
			self.api = self.openVkAPI()

		time.sleep(1)
		return result

	# Scan enter messages and answer
	def run(self):
		while 1:
			time.sleep(1)

			try:
				new_messages = self.api.messages.get(out=0, count=5, time_offset=10)
				del new_messages[0]
				for message in new_messages:
					if message['read_state'] == 0:
						print self.sendAnswer(message)
			except Exception, e:
				print 'Something goes wrong: \n' + str(e)
				self.api = self.openVkAPI()


bot = timebot()
bot.run()
