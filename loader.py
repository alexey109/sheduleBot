#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
import codecs
from os import listdir
from os.path import isfile, join
from optparse import OptionParser

import consts as CONST
import logger as lg
import parser as pr
import dbmodels as db

optparser = OptionParser()
optparser.add_option("-t", "--type", 
	dest="type", 
	help="set schedule type (lections/exams/zachet)", 
	default='lections')
optparser.add_option("-d", "--download", 
	dest="download", 
	help="load docs or not", 
	default=False)
(user_options, args) = optparser.parse_args()

logger = lg.Logger()

if user_options.download:
	logger.log(CONST.LOG_PARSE, "Try to get html code from mirea schedule page.")
	try:
		response = urllib2.urlopen('https://www.mirea.ru/education/schedule-main/schedule/')
		html = response.read()
		logger.log(CONST.LOG_PARSE, 'HTML got succesfull.')
		response.close()
	except Exception as e:
		logger.log(CONST.LOG_PARSE, 'HTML got with errors!')
		logger.log(CONST.LOG_ERROR, e)


	logger.log(CONST.LOG_PARSE, 'Try to load excel documents.')
	counter = 0 
	try:
		doc_urls = re.findall('[^"]*\.xlsx?', html)
		logger.log(CONST.LOG_PARSE, 'Document amount = ' + str(len(doc_urls)))
		for i, url in enumerate(doc_urls):
			ftype = re.search('\.[a-z]*\Z', url).group()
			with open(CONST.SCHEDULE_DIR + str(i) + ftype,'wb') as f:
				f.write(urllib2.urlopen(url).read())
				f.close()
			counter += 1
		logger.log(CONST.LOG_PARSE, 'Document load succesfull. Count = ' + str(counter))
	except Exception as e:
		logger.log(CONST.LOG_PARSE, 'Document load with errors. Last document No ' + str(counter))
		logger.log(CONST.LOG_ERROR, e)


documents = [f for f in listdir(CONST.SCHEDULE_DIR) if isfile(join(CONST.SCHEDULE_DIR, f))]

logger.log(CONST.LOG_PARSE, 'Load schedule to database')
parser = pr.Parser()
print u'Документов:' + str(len(documents))
count = 0 
for doc in documents:
	count += 1
	print u'Загрузка документа №' + str(count) + '\r'
	try:
		schdl_type, schedule = parser.getSchedule(CONST.SCHEDULE_DIR + doc)	
	except:
		continue

	if schdl_type == user_options.type == 'lections':
		for group, events in schedule.items():
			group_obj, flag = db.Groups.get_or_create(gcode = group)
			query = db.Schedule.delete().where(db.Schedule.group == group_obj)
			query.execute()
			for event in events:	
				try:
					nname = event['name']
					for par in event['params']:
						nname += " (" + par + ")"
					nteacher = str(event['teacher']) if event['teacher'] else ''
					nroom = event['room'] if event['room'] else ''
					schdl_obj = db.Schedule(
						group 	= group_obj,
						week 	= event['week'],
						day 	= event['day'],
						numb 	= event['numb'],
						name 	= nname,
						room 	= nroom,
						teacher	= nteacher,
					)
					schdl_obj.save()
				except:
					continue
			

