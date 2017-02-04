#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime as dt
import codecs

import consts as CONST
import re

class Logger:
	def fwrite(self, fname, text):	
		with codecs.open(fname, 'a', 'utf-8') as f:	
			f.write("{};{};{} \n".format(
				dt.datetime.now().strftime('%Y.%m.%d'), 
				dt.datetime.now().strftime('%H:%M:%S'), 
				text) 
			)
			f.close()

	def exception(self, e):
		desc = str(e)
		try:
			if isinstance(e.args[0], int):
				desc = 'Code: %s Text: %s' % (str(e.args[0]), CONST.ERR_MESSAGES[e.args[0]])
		except:
			pass
		fname = CONST.LOG_DIR + CONST.LOG_ERROR_FILE
		self.fwrite(fname, desc)

	def workload(self, text):	
		fname = CONST.LOG_DIR + CONST.LOG_WLOAD_FILE
		self.fwrite(fname, text)

	def feedback(self, text):
		fname = CONST.LOG_DIR + CONST.LOG_FBACK_FILE
		self.fwrite(fname, text)

	def messages(self, text):	
		fname = CONST.LOG_DIR + CONST.LOG_MESGS_FILE
		self.fwrite(fname, text)

	def parser(self, text):	
		fname = CONST.LOG_DIR + CONST.LOG_PARSE_FILE
		self.fwrite(fname, text)
		
	def parser(self, args):	
		fname = CONST.LOG_DIR + CONST.LOG_STATC_FILE
		with codecs.open(fname, 'a', 'utf-8') as f:	
			f.write("%s;%s;%s;%s;%s \n" % (
				dt.datetime.now().strftime('%Y.%m.%d'), 
				dt.datetime.now().strftime('%H:%M:%S'), 
				args[0], 
				re.sub(u'\n', '', args[1]), 
				re.sub(u'\n', '', args[2]))
			)
			f.close()


	def log(self, code, arg):
		if not CONST.LOG:
			return None

		if CONST.TEST:
			print code, arg

		try:
			if code == CONST.LOG_ERROR:
				self.exception(arg)
			elif code == CONST.LOG_WLOAD:
				self.workload(arg)
			elif code == CONST.LOG_FBACK:
				self.feedback(arg)
			elif code == CONST.LOG_MESGS:
				self.messages(arg)
			elif code == CONST.LOG_PARSE:
				self.parser(arg)
			elif code == CONST.LOG_STATC:
				self.parser(arg)
		except:
			pass

