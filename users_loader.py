#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import MySQLdb
from pymongo import MongoClient
import hashlib



import dbmodels as db

db_mongo = MongoClient().timebot

m = hashlib.md5()
m.update(str(vk_id) + str(params['chat_id']) + 'h3d8er3f3')
db_user = db.Users(
	vk_id			= vk_id,
	vk_chat			= bool(params['chat_id']),
	my_id			= m.hexdigest(),
	group			= db_group.id,
	notice_today	= False,
	notice_tommorow	= False,
	notice_week		= False,
	notice_map		= False
)
db_user.save()
