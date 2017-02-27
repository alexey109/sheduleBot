#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import peewee
from peewee import *

import security as sec

db = MySQLDatabase(
	sec.mysql['db'],
	host	= sec.mysql['host'],
	user	= sec.mysql['user'],
	passwd	= sec.mysql['passwd'],
	charset	= sec.mysql['charset'],
	use_unicode = True
)			

class Groups(peewee.Model):
	gcode	= peewee.CharField()
	
	class Meta:
		database = db
		db_table = 'groups'

class Users(peewee.Model):
	vk_id			= peewee.CharField()
	vk_chat			= peewee.BooleanField()
	my_id			= peewee.CharField()
	group			= peewee.ForeignKeyField(Groups)
	notice_today	= peewee.BooleanField()
	notice_tommorow	= peewee.BooleanField()
	notice_week		= peewee.BooleanField()
	notice_map		= peewee.BooleanField()
	
	class Meta:
		database = db
		db_table = 'users'
	
class Schedule(peewee.Model):
	group 	= peewee.ForeignKeyField(Groups)
	week 	= peewee.CharField()
	day 	= peewee.SmallIntegerField()
	numb 	= peewee.SmallIntegerField()
	name 	= peewee.CharField()
	room 	= peewee.CharField()
	teacher	= peewee.CharField()
	
	class Meta:
		database = db
		db_table = 'schedule'
		

class UsersSchedule(peewee.Model):
	user 	= peewee.ForeignKeyField(Users)
	name 	= peewee.CharField()
	day 	= peewee.SmallIntegerField()
	numb 	= peewee.SmallIntegerField()
	teacher	= peewee.CharField()
	week 	= peewee.CharField()
	room 	= peewee.CharField()
	hide	= peewee.BooleanField()
	
	class Meta:
		database = db
		db_table = 'users_schedule'
		

	
