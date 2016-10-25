#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import timebot
import consts as ct
import logger as lg

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
			u'body': u'икбо-06-15 понедельник', 
			u'uid': 10151100, 
			u'title': u'ИКБО-04-15', 
			u'chat_active': 
			u'10151100,294731596', 
			u'mid': 764, 
			u'users_count': 3, 
			u'user_id': 534256,		
			#u'chat_id': 3, 
			u'date': 1475341811, 
			u'admin_id': 10151100, 
			u'read_state': 0, 
			u'out': 0
		},
		'Пар нет :)'
	],
	[	{
			u'uid': 55377,
			u'date': 1477254644,
			u'out': 1,
			u'user_id': 385457066,
			u'read_state': 1,
			u'title': ' ... ',
			u'body': 'завтра',
			u'random_id': -1852873250,
			u'fwd_messages': [{
				u'user_id': 10151100,
				u'date': 1477254617,
				u'body': '',
				u'fwd_messages': [{
					u'user_id': 10151100,
					u'date': 1477252684,
					u'body': u'неделя ИКБО-04-15'
					}]
			}]
		}
	]
]

#bot = timebot.Timebot()
#print bot.getMyAnswer(tests[1][0], False)

logger = lg.Logger()
logger.log(10, 'some error')

