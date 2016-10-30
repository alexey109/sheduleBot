#!/usr/bin/env python
# -*- coding: UTF-8 -*-

STACK_LEN = 10

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

# Commands (CMD)
CMD_AFTERTOMMOROW 	= 120  
CMD_TOMMOROW		= 130 
CMD_YESTERDAY		= 140
CMD_DAY_OF_WEEK 	= 150
CMD_BY_DATE			= 180 #TODO write implementation
CMD_BY_TIME			= 190 #TODO write
CMD_LECTION_NUMB	= 200 

CMD_UNIVERSAL		= 280
CMD_NOW				= 170
CMD_WEEK			= 160 
CMD_TODAY 			= 110
CMD_NEXT 			= 100 
CMD_HELP			= 210
CMD_POLITE			= 220
CMD_LECTIONS_TIME	= 230 
CMD_TEACHER			= 240 
CMD_FIND_LECTION	= 250 #TODO write
CMD_WHEN_EXAMS		= 260 #TODO write	
CMD_FEEDBACK		= 270  

SAVED_GROUP	= 1000

MARKERS = [
	CMD_TOMMOROW,
	CMD_AFTERTOMMOROW,
	CMD_YESTERDAY,
	CMD_DAY_OF_WEEK,
	CMD_LECTION_NUMB,
	CMD_BY_TIME,
	CMD_BY_DATE
]

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
	u'январь?',	
	u'февраль?',
	u'марта?',
	u'апрель?',
	u'майя?',
	u'июнь?',
	u'июль?',
	u'августа?',
	u'сентябрь?',
	u'октябрь?',
	u'ноябрь?',
	u'декабрь?',
]

NUMB_NAMES = [
	u'нулевая',
	u'перва?',
	u'втора?',
	u'третья?',
	u'четверта?',
	u'пята?'
]

# Keywords using when send message from group's chat.
CHAT_KEYWORDS = (
	u'расписание',
	u'бот'
)

# Keywords regexp for every command.
CMD_KEYWORDS = {		
	CMD_FEEDBACK	: [
		u'разработчику', 
		u'предложение', 
		u'ошибка',
		u'можешь сделать'
	],
	CMD_TOMMOROW		: [u'завтра'],
	CMD_NEXT 			: [u'дальше', u'следующ',  u'оставшиеся',  u'остались'],
	CMD_TODAY 			: [u'сегодня'],
	CMD_AFTERTOMMOROW 	: [u'послезавтра'], 
	CMD_YESTERDAY		: [u'вчера'],
	CMD_WEEK			: [u'неделя', u'пройдено' ],
	CMD_NOW				: [u'сейчас', u'текущая'],
	CMD_DAY_OF_WEEK 	: DAY_NAMES,
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
	CMD_POLITE			: [u'спасибо', u'спс'],
	CMD_TEACHER			: [u'кто', u'лектор', u'преподаватель', u'учитель'],
	CMD_LECTIONS_TIME	: [u'время', u'во\s?сколько'],
	CMD_WHEN_EXAMS		: [u'осталось', u'сесси'],
	CMD_BY_TIME			: ['(([01]\d|2[0-3]):([0-5]\d)|24:00)'],
	CMD_BY_DATE			: ['\d{2}\.\d{2}'],
	CMD_FIND_LECTION	: [u'когда[\s\w\\/]*']
}

# Template takes: lection number, classroom, time(start-end), lection name
UNI_TEMPLATE = u'\n%s пара (%s, %s):\n%s\n'
USER_PREMESSAGE = {
	# Parametrs: UNI_TEMPLATE (for all next messages)
	CMD_NEXT 			: u'Следующие пары:\n',
	CMD_TODAY 			: u'Пары сегодня:\n',
	CMD_TOMMOROW		: u'Пары завтра:\n',
	CMD_YESTERDAY		: u'Пары вчера:\n',
	CMD_AFTERTOMMOROW 	: u'Пары послезавтра:\n',
	CMD_WEEK			: '',
	CMD_NOW				: u'Текущая пара:\n',
	CMD_LECTIONS_TIME	: u'Время начала-конца пар\n\n',
	CMD_DAY_OF_WEEK 	: u'Пары в s:\n',
	CMD_FEEDBACK		: u'Сообщение принято и обязательно будет рассмотрено. Спасибо :)',
	CMD_HELP			: u'Инструкция:\nПросто спросите что вы хотите узнать по расписанию пар. '\
		+ u'Если на ваш вопрос нет ответа, то попробуйте спросить по-другому, со временем бот '\
		+ u'научится отвечать на любые формы вопросов.\nПримеры:\n'\
		+ u'"Какие пары завтра?"\n"Следующие лекции"\n"Пары во вторник"\n\n'\
		+ u'В групповой беседе название должно быть указано в теме группы или в каждом сообщении, '\
		+ u'так же надо сначала обратиться боту:\n"Расписание, что завтра у ИКБО-04-15?"\n\n'
		+ u'Более полная инструкция есть на странице бота.',
	CMD_POLITE			: u'Пожалуйста, обращайся ещё :)',
	SAVED_GROUP			: u'Я запомнил группу %s.\n\n',
	CMD_LECTION_NUMB	: u'',
	CMD_TEACHER			: u'Сейчас ведет пару:\n',
	CMD_BY_DATE			: u'Расписание на ',
	CMD_BY_TIME			: u'Пара в ',
	CMD_UNIVERSAL		: ''
}

USER_MESSAGE = {
	CMD_WEEK			: u'Сейчас идет %s неделя.\nПрошло %s семестра.',
}

# Dictionary of lections start-end time for using in messages
LECTION_TIME = {
	1: '9:00-10:35',
	2: '10:45-12:20',
	3: '12:50-14:25',
	4: '14:35-16:10',
	5: '16:20-17:55',
	6: '18:00-21:20',
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
	ERR_UNDEFINED		: u'Что-то пошло не так, повторите запрос еще раз.',
	ERR_SKIP			: '',
	ERR_GROUP_NOT_FOUND	: u'Группа не найдена.\nРасписание для данной группы пока недоступно,'\
		+ u' либо название группы указано с ошибками,.',
	ERR_NO_GROUP		: u'Укажите группу в сообщении или в названии беседы.\nОбразец: ИКБО-04-15',
	ERR_NO_COMMAND		: u'Неизвестная команда.',
	ERR_NO_LECTIONS		: u'Пар нет.',
	ERR_NO_TEACHER		: u'В расписании преподаватель не указан.'
}

