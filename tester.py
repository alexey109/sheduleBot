#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import timebot
import consts as CONST
import logger as lg
import parser as pr
#import clients


# VK API responses
msg = {
	u'count': 50803, 
	u'items': [
		{
			u'body': u'основное', 
			u'user_id': 10151100, 
			u'title': u' ... ', 
			u'date': 1483795240, 
			u'read_state': 1, 
			u'id': 62097, 	
			u'fwd_messages': [		
				{
					u'date': 1483795212, 
					u'body': u'вложенное', 
					u'user_id': 10151100
				}
			], 
			u'out': 0
		}
	]
}

msg_chat = {
	u'count': 50804, 
	u'items': [
		{
			u'body': u'сообщение', 	
			u'user_id': 385457066, 
			u'title': u'Расписание, Алексей_ИКБО-04-15', 
			u'chat_active': [385457066, 294731596], 
			u'users_count': 3, 
			u'chat_id': 27, 
			u'date': 1483795485, 
			u'admin_id': 10151100, 
			u'read_state': 1, 
			u'id': 62099, 
			u'out': 0
		}
	]
}
'''
params = {
	'msg_id'	: 123,
	'user_id'	: 10151100,
	'chat_id'	: 0,
	'text'		: u'завтра 3 пара '
}
answ = timebot.genAnswer(params)
print answ['text'], answ['attachment']
'''


parser = pr.Parser()
schdl_type, res = parser.getSchedule('schedules/IT_2k_16-17_vesna_NOVOE.xlsx')
for g, l in res.items():
	if not g == u'икбо-04-15':
		continue
	for subj in l:	
		'''
		print u"Group: %s, Date: %s, Name: %s, Room: %s, Numb: %s" % (
			g,
			subj['day'],
			subj['name'],	
			subj['room'],
			subj['numb'],
		)

		
		print u"Group: %s, Type: %s, Name: %s, Room: %s, Day: %s, Time: %s" % (
			g,
			subj['type'],
			subj['name'],	
			subj['room'],
			subj['day'],
			subj['time']
		)
		'''
	
		print "Day: %d, Numb: %d, Room: %s, Week: %s, Name: %s, Teacher: %s, Params: s" % (
			subj['day'],		
			subj['numb'],		
			subj['room'],		
			subj['week'],		
			subj['name'],	
			subj['teacher'],
			#str(subj['params']),					
		)
		
		print '----'
	break


