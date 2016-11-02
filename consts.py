#!/usr/bin/env python
# -*- coding: UTF-8 -*-

STACK_LEN = 30

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
CMD_BY_DATE			= 180 
CMD_BY_TIME			= 190
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
CMD_WHEN_EXAMS		= 260
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
	u'среду?',
	u'четверг',
	u'пятницу?',
	u'субботу?',
	u'воскресение'
]

DAY_NAMES_SHORT = [
	u'пн', 
	u'вт',
	u'ср',
	u'чт',
	u'пт',
	u'сб',
	u'вс'
]

MONTH_NAMES = [
	u'январ[яь]',	
	u'феврал[яь]',
	u'мартa?',
	u'апрел[яь]',
	u'майя?',
	u'июн[яь]',
	u'июл[яь]',
	u'августа?',
	u'сентябр[яь]',
	u'октябр[яь]',
	u'ноябр[яь]',
	u'декабр[яь]',
]

NUMB_NAMES = [
	u'нулевая',
	u'перв[аяойи]{2}',
	u'втор[аяойи]{2}',
	u'треть[яейи]{1,2}',
	u'четверт[аяойи]{2}',
	u'пят[аяойи]{2}'
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
	],
	CMD_TOMMOROW		: [u'\sзавтра'],
	CMD_NEXT 			: [u'дальше', u'следующ[аи][яе]',  u'оставш[аи][яи]ся',  u'остал[аи]сь'],
	CMD_TODAY 			: [u'сегодня', u'^\s*расписание$', u'^\s*пар[аы]$'],
	CMD_AFTERTOMMOROW 	: [u'послезавтра'], 
	CMD_YESTERDAY		: [u'вчера'],
	CMD_WEEK			: [u'неделя', u'семестр'],
	CMD_NOW				: [u'сейчас', u'текущая'],
	CMD_DAY_OF_WEEK 	: DAY_NAMES,
	CMD_HELP			: [
		u'инструкци', 
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
	CMD_WHEN_EXAMS		: [u'осталось', u'сесси[ия]', u'прошло', u'пройден'],
	CMD_BY_TIME			: ['(([01]?\d|2[0-3]):([0-5]\d)|24:00)'],
	CMD_BY_DATE			: ['(\d{1,2}\.\d{2})|(\d{1,2}\s*((' + ")|(".join(MONTH_NAMES) + ')))'],
	#CMD_FIND_LECTION	: [u'когда[\s\w\\/]*']
}

# Template takes: lection number, classroom, time(start-end), lection name
UNI_TEMPLATE = u'\n{} пара ({}, {}):\n{}\n'
USER_PREMESSAGE = {
	# Parametrs: UNI_TEMPLATE (for all next messages)
	CMD_UNIVERSAL		: u'Пары{markers}:\n',
	CMD_TOMMOROW		: u' завтра',
	CMD_YESTERDAY		: u' вчера',
	CMD_AFTERTOMMOROW 	: u' послезавтра',
	CMD_DAY_OF_WEEK 	: u' в {}',
	CMD_BY_DATE			: u' {}',
	CMD_BY_TIME			: u' в {}',
	CMD_LECTION_NUMB	: u' номер {}',

	CMD_WEEK			: '',
	CMD_NEXT 			: u'Следующие пары:\n',
	CMD_TODAY 			: u'Пары сегодня{markers}:\n',
	CMD_NOW				: u'Текущая пара:\n',
	CMD_LECTIONS_TIME	: u'Время начала-конца пар\n\n',
	CMD_FEEDBACK		: u'Сообщение принято и обязательно будет рассмотрено. Спасибо :)',
	CMD_HELP			: u'Инструкция:\nПросто спросите что вы хотите узнать по расписанию пар. '\
		+ u'Если на ваш вопрос нет ответа, то попробуйте спросить по-другому, со временем бот '\
		+ u'научится отвечать на любые формы вопросов.\n\n'\
		+ u'Во избежании капчи и блокировки добавлены ограничения:\n'\
		+ u'- бот отвечает только на понятные ему сообщения.\n'\
		+ u'- бот НЕ ПИШЕТ один и тот же ответ больше ОДНОГО раза.\n'\
		+ u'\nПримеры:\n'\
		+ u'"Какие пары завтра?"\n"Следующие лекции."\n"Пары во вторник."\n\n'\
		+ u'Полная инструкция есть на странице бота.\n\n',
	CMD_POLITE			: u'Пожалуйста, обращайся ещё :)',
	SAVED_GROUP			: u'Я запомнил группу {}.\n\n',
	CMD_TEACHER			: u'Преподаватель на паре{markers}:\n',
	CMD_WHEN_EXAMS		: u'Зачетная неделя, ориентировочно, с 19 декабря. \n',
	CMD_FIND_LECTION	: u''
}

USER_MESSAGE = {
	CMD_WEEK			: u'Сейчас идет {} неделя.',	
	CMD_LECTIONS_TIME	: u'{} пара: {}\n',
	CMD_WHEN_EXAMS		: u'Осталось {} недель {} дней.\nСеместр завершен на {}.'
}

# Dictionary of lections start-end time for using in messages
LECTION_TIME = {
	1: '9:00-10:35',
	2: '10:45-12:20',
	3: '12:50-14:25',
	4: '14:35-16:10',
	5: '16:20-17:55',
	6: '18:00-19:35',
	7: '19:45-21:20'
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
	ERR_GROUP_NOT_FOUND	: u'Группа не найдена.\nРасписание для данной группы недоступно,'\
		+ u' либо название группы указано с ошибками,.',
	ERR_NO_GROUP		: u'Напишите из какой вы группы.\nОбразец: расписание, ИКБО-04-15',
	ERR_NO_COMMAND		: u'Неизвестная команда.',
	ERR_NO_LECTIONS		: u'Пар нет.',
	ERR_NO_TEACHER		: u'В расписании преподаватель не указан.'
}

