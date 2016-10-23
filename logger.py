#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime as dt

import consts as ct

class Logger:
	def fwrite(self, fname, text):	
		with open(fname, 'a') as f:		
			f.write('%s: %s \n' % (dt.datetime.now(), text) )
			f.close()

	def exception(self, e):
		desc = str(e)
		if isinstance(e.args[0], int):
			desc = 'Code: %s Text: %s' % (e.args[0], ct.CONST.ERR_MESSAGES[e.args[0]])

		fname = ct.CONST.LOG_DIR + ct.CONST.LOG_ERROR_FILE
		self.fwrite(fname, decs)

	def workload(self, text):	
		fname = ct.CONST.LOG_DIR + ct.CONST.LOG_WLOAD_FILE
		self.fwrite(fname, text)

	def feedback(self, text):	
		fname = ct.CONST.LOG_DIR + ct.CONST.LOG_FBACK_FILE
		self.fwrite(fname, text)

	def messages(self, text):	
		fname = ct.CONST.LOG_DIR + ct.CONST.LOG_MESGS_FILE
		self.fwrite(fname, text)

	def parser(self, text):	
		fname = ct.CONST.LOG_DIR + ct.CONST.LOG_PARSE_FILE
		self.fwrite(fname, text)


	def log(self, code, arg):
		if not ct.CONST.LOG:
			return None

		try:
			if code == ct.CONST.LOG_ERROR:
				self.exception(arg)
			elif code == ct.CONST.LOG_WLOAD:
				self.workload(arg)
			elif code == ct.CONST.LOG_FBACK:
				self.feedback(arg)
			elif code == ct.CONST.LOG_MESGS:
				self.messages(arg)
			elif code == ct.CONST.LOG_PARSE:
				self.parser(arg)
		except:
			pass

