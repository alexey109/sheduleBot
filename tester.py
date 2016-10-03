#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import timebot
import consts as ct

# Test vk api responses
'''
tests = [
	[
		{
			u'body': u'пары в пятницу у КТСО-04-15', 
			u'uid': 10151100, 
			u'title': u'ИКБО-04-15', 
			u'chat_active': 
			u'10151100,294731596', 
			u'mid': 764, 
			u'users_count': 3, 
			u'chat_id': 3, 
			u'date': 1475341811, 
			u'admin_id': 10151100, 
			u'read_state': 0, 
			u'out': 0
		},
		'5'
	],
	[
		{
			u'body': u'пары дальше ИКБО-04-15', 
			u'uid': 10151100, 
			u'title': u'ИКБО-04-15', 
			u'chat_active': 
			u'10151100,294731596', 
			u'mid': 764, 
			u'users_count': 3, 
			u'chat_id': 3, 
			u'date': 1475341811, 
			u'admin_id': 10151100, 
			u'read_state': 0, 
			u'out': 0
		},
		'Пар нет :)'
	],
]
'''

tests = [
	[
		{
			u'body': u'завтра ИКБО-04-15', 
			u'uid': 10151100, 
			u'title': u'ИКБО-04-15', 
			u'chat_active': 
			u'10151100,294731596', 
			u'mid': 764, 
			u'users_count': 3, 
			u'chat_id': 3, 
			u'date': 1475341811, 
			u'admin_id': 10151100, 
			u'read_state': 0, 
			u'out': 0
		},
		'Пар нет :)'
	]
]

bot = timebot.Timebot()
for i, test in enumerate(tests):
	#print 'Test %, result %' % (i, test[1] == bot.getMyAnswer(message))
	result = bot.getMyAnswer(test[0], False)
	print result


