#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import peewee
from peewee import *

import security as SEC

db = MySQLDatabase(
    SEC.mysql['db'],
    host=SEC.mysql['host'],
    user=SEC.mysql['user'],
    passwd=SEC.mysql['passwd'],
    charset=SEC.mysql['charset'],
    use_unicode=True
)


class Groups(peewee.Model):
    gcode = peewee.CharField()

    class Meta:
        database = db
        db_table = 'groups'


class Users(peewee.Model):
    vk_id = peewee.CharField()
    is_chat = peewee.BooleanField()
    bot_id = peewee.CharField()
    group = peewee.ForeignKeyField(Groups)
    notice_today = peewee.BooleanField()
    notice_tommorow = peewee.BooleanField()
    notice_week = peewee.BooleanField()
    notice_map = peewee.BooleanField()
    send_time = peewee.DateTimeField()
    notice_zerohour = peewee.DateTimeField()
    bot_activity = peewee.DateTimeField()

    class Meta:
        database = db
        db_table = 'users'


class Schedule(peewee.Model):
    group = peewee.ForeignKeyField(Groups)
    week = peewee.CharField()
    day = peewee.SmallIntegerField()
    numb = peewee.SmallIntegerField()
    name = peewee.CharField()
    room = peewee.CharField()
    teacher = peewee.CharField()

    class Meta:
        database = db
        db_table = 'schedule'


class UsersSchedule(peewee.Model):
    user = peewee.ForeignKeyField(Users)
    name = peewee.CharField()
    day = peewee.SmallIntegerField()
    numb = peewee.SmallIntegerField()
    teacher = peewee.CharField()
    week = peewee.CharField()
    room = peewee.CharField()
    hide = peewee.BooleanField()

    class Meta:
        database = db
        db_table = 'users_schedule'


class Scheme(peewee.Model):
    photo_id = peewee.CharField()
    old_photo_id = peewee.CharField()
    name = peewee.CharField()
    name_ru = peewee.CharField()
    rooms = peewee.CharField()
    desc = peewee.CharField()

    class Meta:
        database = db
        db_table = 'schemes'
