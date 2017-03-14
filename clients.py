#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk
import time

import security
import timebot as bot
import logger as lg
import consts as CONST


def waitNextCall(lastCall, delta):
	while (time.time() - lastCall) < delta:
		time.sleep(0.3)	

class UsersStack:
	def __init__(self):
		self.stack = []
	
	def getRest(self, user_id):
		now = int(time.time())
		try:
			while (now - self.stack[0][1]) >= CONST.USERS_QUEUE_LEN:
				del self.stack[0]
		except:
			pass
		
		user_time = [user_id, now]	
		amount = 0
		max_time = 0
		for rec in self.stack:
			if rec[0] == user_time[0]:
				tdiff = now - rec[1]
				if tdiff > max_time:
					max_time = tdiff
				amount += 1
		
		rest = CONST.USER_MSG_AMOUNT - amount
		if rest > 0 :
			self.stack.append(user_time)

		return rest, CONST.USERS_QUEUE_LEN - max_time
		

class ClientVK:

	def __init__(self):
		self.logger    		= lg.Logger()
		self.last_call 		= 0
		self.usr_stack 		= UsersStack()

	# Open vkAPI session
	# Return type: vk.api object
	def openSession(self):
		success = False
		while not success:
			try:
				session = vk.AuthSession(
					app_id = security.app_id, 
					user_login = security.user_login, 
					user_password = security.user_password, 
					scope = security.scope)
				api = vk.API(session, v='5.60', lang='ru')
				success = True
			except Exception as e:
				self.logger.log(CONST.LOG_ERROR, e)
				time.sleep(3)
		return api

	def retriveBody(self, vk_msg):
		body = vk_msg.get('body', '')
		fwd_messages = vk_msg.get('fwd_messages', [])
		for msg in fwd_messages:
			body += ' ' + self.retriveBody(msg) + ' '

		return body

	# Send answer for enter message
	# Return type: string 
	def sendMyAnswer(self, vk_msg):
		answer = {
			'text'		: '',
			'attachment': ''
		}

		msg_text = self.retriveBody(vk_msg)
		params = {
			'msg_id'	: vk_msg['id'],
			'user_id'	: vk_msg.get('user_id', 0),
			'chat_id'	: vk_msg.get('chat_id', 0),
			'text'		: msg_text
		}

		if not params['chat_id']:
			waitNextCall(self.last_call, 0.5)
			self.api.messages.markAsRead(message_ids=params['msg_id'], peer_id=params['user_id'])

		try:
			answer = bot.genAnswer(params)
		except Exception as e:
			if isinstance(e.args[0], int):
				answer['text'] = CONST.ERR_MESSAGES[e.args[0]]
			else:
				self.logger.log(CONST.LOG_ERROR, e)
				answer['text'] = CONST.ERR_MESSAGES[CONST.ERR_UNDEFINED]

		if answer['text'] or answer['attachment']: 
			fullmsg = str(params['user_id']) + answer['text'] + answer['attachment'] 
			msg_rest, time_rest = self.usr_stack.getRest(params['user_id'])
			if (msg_rest == 0):
				return
			if msg_rest == 1:
				answer['text'] += CONST.ERR_MESSAGES[CONST.ERR_MSG_LIMIT].format(time_rest)
			self.logger.log(CONST.LOG_STATC, [params['user_id'], msg_text, answer['text'][:100]])
			
			waitNextCall(self.last_call, 1)
			if params['chat_id']:
				self.api.messages.send(
					chat_id = params['chat_id'], 
					message = answer['text'], 
					attachment = answer['attachment']
				)
			else:
				self.api.messages.send(
					user_id = params['user_id'], 
					message = answer['text'], 
					attachment = answer['attachment']
				)
			
			self.last_call = time.time()	

	def sendNotice(self, notice):
		waitNextCall(self.last_call, CONST.NOTICE_DELAY)
		if notice['is_chat']:
			self.api.messages.send(
				chat_id = notice['user_id'], 
				message = notice['text'], 
				attachment = notice['attachment']
			)
		else:
			self.api.messages.send(
				user_id = notice['user_id'], 
				message = notice['text'], 
				attachment = notice['attachment']
			)
		bot.saveNoticeTime(notice)
		
		self.last_call = time.time()

	# Scan enter messages and answer
	def run(self):		
		self.api = self.openSession()
		last_get_call = time.time() - 10
		toffset = time.time()
		while 1:
			try:
				waitNextCall(self.last_call, 1)
				toffset = int(time.time() - last_get_call)
				toffset = toffset if toffset > 10 else 10
				response = self.api.messages.get(out=0, count=10, time_offset=toffset, preview_length=100)
				self.last_call 	= time.time()
				last_get_call	= time.time()
				unread_msgs = []
				for vk_msg in response['items']:
					if vk_msg['read_state'] == 0:
						unread_msgs.append(vk_msg)
				if unread_msgs:
					for vk_msg in unread_msgs:
						try:
							self.sendMyAnswer(vk_msg)
						except Exception as e:
							self.logger.log(CONST.LOG_ERROR, e)
							self.api = self.openSession()
				elif bot.isNoticeTime():
					try:
						self.sendNotice(bot.getNotice())
					except:
						pass
						
			except Exception as e:
				print str(e)
				print 'Exception! Try to open new session'
				self.logger.log(CONST.LOG_ERROR, e)
				self.api = self.openSession()
				print 'Session was opened'


vk_client = ClientVK()
vk_client.run()
