#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import timebot

# Test vk api responses
vk_response = (
	[
		1, 
		{
			u'body': u'Пары сегодня', 
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
		{
			u'body': u'Пары сегодня', 
			u'uid': 10151100, 
			u'title': u' ... ', 
			u'mid': 763, 
			u'date': 1475341804, 
			u'read_state': 0, 
			u'out': 0
		}
	],
	[
		3, 
		{
			u'body': u'Пары послезавтра', 
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
		{
			u'body': u'Пары послезавтра', 
			u'uid': 10151100, 
			u'title': u' ... ', 
			u'mid': 763, 
			u'date': 1475341804, 
			u'read_state': 0, 
			u'out': 0
		}
	],
	[
		4, 
		{
			u'body': u'Пары в понедельник', 
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
		{
			u'body': u'Пары в понедльник', 
			u'uid': 10151100, 
			u'title': u' ... ', 
			u'mid': 763, 
			u'date': 1475341804, 
			u'read_state': 0, 
			u'out': 0
		}
	],
	[
		5, 
		{
			u'body': u'Пары в пятницу', 
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
		{
			u'body': u'Пары в пятницу', 
			u'uid': 10151100, 
			u'title': u' ... ', 
			u'mid': 763, 
			u'date': 1475341804, 
			u'read_state': 0, 
			u'out': 0
		}
	],
	[
		6, 
		{
			u'body': u'Пары в понедельник у ИКБО-04-15', 
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
		{
			u'body': u'Пары в понедельник у ИКБО-04-15', 
			u'uid': 10151100, 
			u'title': u' ... ', 
			u'mid': 763, 
			u'date': 1475341804, 
			u'read_state': 0, 
			u'out': 0
		}
	],
	[
		7, 
		{
			u'body': u'Лекции послезавтра у ИКБО-08-16', 
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
		{
			u'body': u'Лекции послезавтра у ИКБО-08-16', 
			u'uid': 10151100, 
			u'title': u' ... ', 
			u'mid': 763, 
			u'date': 1475341804, 
			u'read_state': 0, 
			u'out': 0
		}
	],
	[
		8, 
		{
			u'body': u'Лекции в субботу у ИКБО-08-16', 
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
		{
			u'body': u'Лекции в субботу у ИКБО-08-16', 
			u'uid': 10151100, 
			u'title': u' ... ', 
			u'mid': 763, 
			u'date': 1475341804, 
			u'read_state': 0, 
			u'out': 0
		}
	]
)


bot = timebot.timebot()
for i, test in enumerate(vk_response):
	print '\n\nTest No', i, '(',test[0], ')', '-------------------------------'
	del test[0]
	for message in test:
		if message['read_state'] == 0:
			print 'Title: ', message['title'], ' Body:', message['body'], '\n'
			print bot.getLections(message['title'], message['body'])

