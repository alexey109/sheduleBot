#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime as dt
import time
import string
import vk
import sys
import re
import codecs
from pymongo import MongoClient

import parser 
import consts as ct


# Class implement bot logic. The main idea of this bot to help everyone with schedule.
# Bot intergated to socialnet and like a friend can tell you what next lection you will have.
# Normal documentation will be in future.
class Timebot:
	def __init__(self):
		self.table = parser.Schedule()
		self.db = MongoClient().timebot

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
	def listToStr(self, params):
		if params == []:
			raise Exception(ct.CONST.ERR_NO_LECTIONS)

		result = ''
		for row in params:
			result += ct.CONST.UNI_TEMPLATE % (row)
		return result

	# Return tommorow lections
	# Return type: string
	def getTommorowLections(self, group_name):
		day_numb = (dt.datetime.today() + dt.timedelta(days=1)).weekday()
		week_numb = (dt.datetime.now() + dt.timedelta(days=1)).isocalendar()[1]

		return self.listToStr(self.table.getLections(group_name, day_numb, week_numb))

	# Return after tommorow lections
	# Return type: string
	def getAfterTommorowLections(self, group_name):
		day_numb = (dt.datetime.today() + dt.timedelta(days=2)).weekday()
		week_numb = (dt.datetime.now() + dt.timedelta(days=2)).isocalendar()[1]

		return self.listToStr(self.table.getLections(group_name, day_numb, week_numb))

	# Return today lections
	# Return type: string
	def getTodayLections(self, group_name):
		day_numb = dt.datetime.today().weekday()
		week_numb = dt.datetime.now().isocalendar()[1]
	
		return self.listToStr(self.table.getLections(group_name, day_numb, week_numb))

	# Return today next lection
	# Return type: string
	def getNextLections(self, group_name):
		week_numb = dt.datetime.now().isocalendar()[1]
		lection_start = int(self.lectionFromTime(dt.datetime.now().time())) + 1
		if lection_start == 7:
			day_numb = (dt.datetime.today() + dt.timedelta(days=1)).weekday()
		else:
			day_numb = dt.datetime.today().weekday()
	
		return self.listToStr(self.table.getLections(group_name, day_numb, week_numb,lection_start))

	# Return lections for selected day
	# Return type: string
	def getLectionsByDay(self, group_name, day_numb):
		week_numb = dt.datetime.now().isocalendar()[1]
		if dt.datetime.today().weekday() >= day_numb:
			week_numb += 1
			
		return self.listToStr(self.table.getLections(group_name, day_numb, week_numb))

	# Return current week number
	# Return type: string
	def getWeekNumb(self):
		week_numb = dt.datetime.now().isocalendar()[1] - dt.date(2016, 9, 1).isocalendar()[1] + 1
		return str(week_numb)

	# Return today lections
	# Return type: string
	def getNowLection(self, group_name):
		day_numb = dt.datetime.today().weekday()
		week_numb = dt.datetime.now().isocalendar()[1]
		lection = int(self.lectionFromTime(dt.datetime.now().time()))
	
		return self.listToStr(self.table.getLections(group_name,day_numb,week_numb,lection,lection))


	# Get group name from any string
	# Return type: string
	def getGroupFromString(self, string):
		match = re.search(u'[а-я]{4}-[0-9]{2}-[0-9]{2}', string)
		return match.group(0) if match else ''
		
	# Check is any word in text
	# Return type: boolean
	def wordsInTxt(self, words, text):
		return any(word[:-1] in text for word in words)


	# Takes message and prepare answer for it.
	# Return type: string
	def getMyAnswer(self, message, is_chat):
		answer = ''
		title = message['title'].lower()
		text = message['body'].lower()

		if is_chat and not self.wordsInTxt(ct.CONST.CHAT_KEYWORDS, text):
			raise Exception(ct.CONST.ERR_SKIP)

		group_from_title = self.getGroupFromString(title)
		group_from_msg = self.getGroupFromString(text)
		if group_from_msg:		
			group_name = group_from_msg
		elif group_from_title:
			group_name = group_from_title		
		elif is_chat:
			raise Exception(ct.CONST.ERR_NO_GROUP_NAME)

		if not is_chat:
			try:
				group_name = self.db.users.find({'vk_id':message['uid']})[0]['group_name']
				if group_from_msg
					self.db.users.update_one(
						{'vk_id':message['uid']},
						{'$set': {'group_name': group_from_msg}}
					)
					answer += ct.CONST.USER_PREMESSAGE[ct.CONST.SAVED_GROUP_NAME] % (group_from_msg)
			except:
				if group_from_msg:
					self.db.users.insert_one({'vk_id': message['uid'], 'group_name': group_from_msg}):
					answer += ct.CONST.USER_PREMESSAGE[ct.CONST.SAVED_GROUP_NAME] % (group_from_msg)
				else:
					raise Exception(ct.CONST.ERR_NO_GROUP_NAME)	
			
		group_name = group_name.upper()

		for command, keywords in ct.CONST.CMD_KEYWORDS.items():
			if self.wordsInTxt(keywords, text):		
				template = ct.CONST.USER_PREMESSAGE[command]
				if command == ct.CONST.CMD_NEXT:
					answer += template % (self.getNextLections(group_name))
				elif command == ct.CONST.CMD_TODAY:
					answer += template % (self.getTodayLections(group_name))
				elif command == ct.CONST.CMD_AFTERTOMMOROW:
					answer += template % (self.getAfterTommorowLections(group_name))
				elif command == ct.CONST.CMD_TOMMOROW:
					answer += template % (self.getTommorowLections(group_name))
				elif command == ct.CONST.CMD_WEEK_NUMB:
					answer += template % (self.getWeekNumb())
				elif command == ct.CONST.CMD_NOW:
					answer += template % (self.getNowLection(group_name))
				elif command == ct.CONST.CMD_TO_DEVELOPER:
					with codecs.open('msg_to_me.txt', mode='a', encoding='utf-8') as txt_file:
						txt_file.write('\n' + text + '\n')
					answer += ct.CONST.USER_PREMESSAGE[ct.CONST.CMD_TO_DEVELOPER]
				elif command == ct.CONST.CMD_DAY_OF_WEEK:
					for day_idx, day_name in enumerate(keywords):
						if day_name[:-1] in text:
							answer += template % (day_name, self.getLectionsByDay(group_name, day_idx))
							break
				else:
					raise Exception(ct.CONST.ERR_UNDEFINED)
				break
		if not answer:
			raise Exception(ct.CONST.ERR_NO_COMMAND)
		
		return answer
				
			

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
	# TODO Add status code, or use boolean.
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
					print str(e)

			if my_answer: 
				if is_chat:
					self.api.messages.send(chat_id=message['chat_id'], message=my_answer)
				else:
					self.api.messages.send(user_id=message['uid'], message=my_answer)
				print 'Message send.'
				time.sleep(1)
		except Exception, e:
			print 'Message not send: \n' + str(e)
			self.api = self.openVkAPI()

	# Scan enter messages and answer
	def run(self):		
		self.api = self.openVkAPI()
		while 1:
			time.sleep(1)
			try:
				new_messages = self.api.messages.get(out=0, count=5, time_offset=15)	
				del new_messages[0]
				for message in new_messages:
					if message['read_state'] == 0:
						self.sendMyAnswer(message)
			except Exception, e:
				print 'Error code: ' + str(e)
				self.api = self.openVkAPI()


bot = Timebot()
bot.run()
