#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
import codecs
from os import listdir
from os.path import isfile, join
from optparse import OptionParser
import MySQLdb

import consts as CONST
import logger as lg
import parser as pr
import security as sec

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

dbMySQL = MySQLdb.connect(
	host =	sec.mysql['host'],
	user =	sec.mysql['user'],
	passwd =sec.mysql['passwd'],
	db =	sec.mysql['db'],
	charset=sec.mysql['charset'],
	use_unicode=True
)
					
curMySQL = dbMySQL.cursor()

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
		for group in schedule:
			upd = 0
		
			curMySQL.execute("SELECT * FROM groups WHERE gcode = '{}';".format(group.encode('utf-8')))
			try:
				gid, gcode = curMySQL.fetchone();
				curMySQL.execute("DELETE FROM schedule WHERE group_id={};".format(gid))
				dbMySQL.commit()
				curMySQL.execute("DELETE FROM groups WHERE gcode='{}';".format(group.encode('utf-8')))
				dbMySQL.commit()
			except:
				pass
			curMySQL.execute("INSERT INTO groups (gcode) VALUES ('{}');".format(group.encode('utf-8')))
			dbMySQL.commit()
			curMySQL.execute("SELECT * FROM groups WHERE gcode = '{}';".format(group.encode('utf-8')))
			gid, gcode = curMySQL.fetchone();
			for event in schedule[group]:	
				try:	
					name = event['name']
					teacher = str(event['teacher']).encode('utf-8') if event['teacher'] else ''
					room = event['room'].encode('utf-8') if event['room'] else ''
					for par in event['params']:
						name += " (" + par + ")"
					query = "INSERT INTO schedule (group_id, week, day, numb, name, room, teacher) VALUES ({},'{}',{},{},'{}','{}','{}');".format(
						gid, 
						event['week'].encode('utf-8'), 
						event['day'], 
						event['numb'], 
						name.encode('utf-8'), 
						room, 
						teacher[:59]
					)				
					curMySQL.execute(query)
				except:
					continue
			dbMySQL.commit()
			
			
dbMySQL.close()

