#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
import codecs
from pymongo import MongoClient
from os import listdir
from os.path import isfile, join

import consts as CONST
import logger as lg
import parser as pr

logger = lg.Logger()

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


db = MongoClient().timebot
documents = [f for f in listdir(CONST.SCHEDULE_DIR) if isfile(join(CONST.SCHEDULE_DIR, f))]

logger.log(CONST.LOG_PARSE, 'Load schedule to database')
parser = pr.Parser()
for doc in documents:
	schedule = parser.getSchedule(CONST.SCHEDULE_DIR + doc)	
	for group in schedule:
		try:
			a = db.schedule.find({'group':group})[0]['schedule']
			db.schedule.update_one({'group': group},{'$set':{'schedule': schedule[group]}})
		except:
			db.schedule.insert_one({'group': group, 'schedule': schedule[group]})



