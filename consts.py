#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# There is all constant values used by all project classes.
class CONST:
	# Enable/disable logging everything.
	LOG	 = True
	LOG_DIR = 'log/'

	# Log type codes
	LOG_ERROR	= 10
	LOG_WLOAD	= 20
	LOG_FBACK	= 30
	LOG_MESGS	= 40
	LOG_PARSE	= 50

	# Log file names
	LOG_ERROR_FILE 	= 'exceptions.txt'
	LOG_WLOAD_FILE  = 'workload.txt'
	LOG_FBACK_FILE	= 'feedback.txt'
	LOG_MESGS_FILE	= 'messages.txt'
	LOG_PARSE_FILE	= 'parser.txt'

	# Enable/disable test mode
	TEST = False

	SCHEDULE_DIR = 'schedules/'

	# Commands (CMD) Order is important
	CMD_TO_DEVELOPER	= 100 
	CMD_NEXT 			= 110
	CMD_TODAY 			= 120
	CMD_AFTERTOMMOROW 	= 130 # It is important to be aftertommorow before tomorrow :)
	CMD_TOMMOROW		= 140
	CMD_DAY_OF_WEEK 	= 150
	CMD_WEEK			= 160 # It is important to be aftertommorow before current lection :)
	CMD_NOW				= 170 
	CMD_HELP			= 180 
	CMD_STARTTIME		= 190 #TODO write implementation
	CMD_ENDTIME			= 200 #TODO write implementation
	CMD_LECTION_NUMB	= 210 
	CMD_POLITE			= 220
	CMD_LECTION_TIME	= 230 
	CMD_HELLO			= 240 
	CMD_YESTERDAY		= 250 
	CMD_DATE			= 260 #TODO write implementation
	CMD_GROUP			= 270 #TODO write implementation ???
	CMD_TEACHER			= 280 

	SAVED_GROUP	= 1000

	DAY_NAMES = [
		u'понедельник', 
		u'вторник',
		u'среду',
		u'четверг',
		u'пятницу',
		u'субботу',
		u'воскресение'
	]

	MONTH_NAMES = [
		u'январь',	
		u'февраль',
		u'март',
		u'апрель',
		u'май',
		u'июнь',
		u'июль',
		u'август',
		u'сентябрь',
		u'октябрь',
		u'ноябрь',
		u'декабрь',
	]

	NUMB_NAMES = [
		u'нулевая+',
		u'перв+',
		u'втора+',
		u'треть+',
		u'четверт+',
		u'пятая+'
	]

	# Dictionary of lections start-end time for using in messages
	LECTION_TIME = {
		1: '9:00-10:35',
		2: '10:45-12:20',
		3: '12:50-14:25',
		4: '14:35-16:10',
		5: '16:20-17:55',
		6: '18:00-21:20',
	}

	# Keywords using when send message from group's chat.
	CHAT_KEYWORDS = (
		u'расписание+',
		u'бот+'
	)
	# Keywords for every command.
	CMD_KEYWORDS = {
		CMD_NEXT 			: [u'дальше', u'следующ+',  u'оставшиеся',  u'остались'],
		CMD_TODAY 			: [u'сегодня'],
		CMD_AFTERTOMMOROW 	: [u'послезавтра'], 
		CMD_TOMMOROW		: [u'завтра'],
		CMD_YESTERDAY		: [u'вчера'],
		CMD_WEEK			: [u'неделя+', u'пройден+' ],
		CMD_NOW				: [u'сейчас', u'текущая'],
		CMD_DAY_OF_WEEK 	: DAY_NAMES,
		CMD_TO_DEVELOPER	: [
			u'разработчику', 
			u'предложение', 
			u'ошибка',
		],
		CMD_HELP			: [
			u'инструкция', 
			u'справка', 
			u'помощь',
			u'help', 
			u'работаешь', 
			u'пользоваться',
			u'умеешь',
			u'делаешь',
			u'команды'
		],
		CMD_LECTION_NUMB	: NUMB_NAMES,
		CMD_POLITE			: [u'спасибо'],
		CMD_HELLO			: [u'привет'],
		CMD_TEACHER			: [u'кто+', u'лектор', u'преподаватель', u'учитель'],
		CMD_LECTION_TIME	: [u'время', u'расписание', u'во сколько']
	}

	# Template takes: lection number, classroom, time(start-end), lection name
	UNI_TEMPLATE = u'\n%s пара (%s, %s):\n%s\n'
	USER_PREMESSAGE = {
		# Parametrs: UNI_TEMPLATE (for all next messages)
		CMD_NEXT 			: u'Следующие пары:\n%s',
		CMD_TODAY 			: u'Пары сегодня:\n%s',
		CMD_TOMMOROW		: u'Пары завтра:\n%s',
		CMD_YESTERDAY		: u'Пары вчера:\n%s',
		CMD_AFTERTOMMOROW 	: u'Пары послезавтра:\n%s',
		CMD_WEEK			: u'Сейчас идет %s неделя.\nПрошло %s семестра.',
		CMD_NOW				: u'Текущая пара:\n%s',
		CMD_LECTION_TIME	: u'Время начала-конца пар\n\n%s',
		CMD_DAY_OF_WEEK 	: u'Пары в %s:\n%s', # One new parametr: day of week
		CMD_TO_DEVELOPER	: u'Сообщение принято и обязательно будет рассмотрено, спасибо :)',
		CMD_HELP			: u'Инструкция:\nПросто спросите что вы хотите узнать по расписанию пар. '\
			+ u'Если на ваш вопрос нет ответа, то попробуйте спросить по-другому, со временем бот '\
			+ u'научится отвечать на любые формы вопросов.\nПримеры:\n'\
			+ u'"Какие пары завтра?"\n"Следующие лекции"\n"Пары во вторник"\n\n'\
			+ u'В групповой беседе название должно быть указано в теме группы или в каждом сообщении, '\
			+ u'так же надо сначала обратиться боту:\n"Расписание, что завтра у ИКБО-04-15?"\n\n'
			+ u'Более полная инструкция есть на странице бота.',
		CMD_POLITE			: u'Пожалуйста, обращайся ещё :)',
		SAVED_GROUP			: u'Я запомнил, что ты из %s.\n\n',
		CMD_LECTION_NUMB	: u'%s\nP.S. пара сегодня',
		CMD_HELLO			: u'Привет ;)',
		CMD_TEACHER			: u'Сейчас ведет пару:\n%s'
	}

	# Error codes, will raise as exceptions.
	ERR_UNDEFINED 		= 0
	ERR_SKIP			= 1
	ERR_GROUP_NOT_FOUND = 2
	ERR_NO_GROUP		= 3
	ERR_NO_COMMAND		= 4
	ERR_NO_LECTIONS		= 5
	ERR_NO_TEACHER		= 6
	
	ERR_MESSAGES = {
		ERR_UNDEFINED: u'Что-то пошло не так, повторите запрос еще раз :(',
		ERR_SKIP: '',
		ERR_GROUP_NOT_FOUND: u'Группа не найдена.\nРасписание для данной группы пока недоступно,'\
			+ u' либо название группы указано с ошибками,.',
		ERR_NO_GROUP: u'Укажите группу в сообщении или в названии беседы.\nОбразец: ИКБО-04-15',
		ERR_NO_COMMAND: u'Неизвестная команда.',
		ERR_NO_LECTIONS: u'Пар нет.',
		ERR_NO_TEACHER: u'В расписании преподаватель не указан.'
	}
