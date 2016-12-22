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
CMD_TODAY 			= 110
CMD_NOW				= 170

CMD_UNIVERSAL		= 280
CMD_NEXT 			= 100
CMD_WEEK			= 160 
CMD_HELP			= 210
CMD_POLITE			= 220
CMD_LECTIONS_TIME	= 230 
CMD_TEACHER			= 240 
CMD_FIND_LECTION	= 250 #TODO write
CMD_WHEN_EXAMS		= 260
CMD_FEEDBACK		= 270  
CMD_MYGROUP			= 290
CMD_SAVE_GROUP		= 300
CMD_MAP				= 310
CMD_EXAMS			= 320
CMD_CONSULT			= 330
CMD_SESSION			= 340
CMD_CALENDAR_JN		= 350
CMD_CALENDAR_DC		= 360
CMD_ZACHET			= 370
CMD_WHERE			= 380


MARKERS = [
	CMD_NOW,
	CMD_TODAY,
	CMD_TOMMOROW,
	CMD_AFTERTOMMOROW,
	CMD_YESTERDAY,
	CMD_DAY_OF_WEEK,
	CMD_LECTION_NUMB,
	CMD_BY_TIME,
	CMD_BY_DATE
]

DAY_NAMES = [
	u'((\s|\A)пн(\s|\Z))|(понедельник)', 
	u'((\s|\A)вт(\s|\Z))|(вторник)',
	u'((\s|\A)ср(\s|\Z))|(сред[ау])',
	u'((\s|\A)чт(\s|\Z))|(четверг)',
	u'((\s|\A)пт(\s|\Z))|(пятниц[ау])',
	u'((\s|\A)сб(\s|\Z))|(суббот[ау])',
	u'((\s|\A)вс(\s|\Z))|(воскресение)'
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
	u'((\s|\A)0(\s|\Z))|(нулевая)',
	u'((\s|\A)1(\s|\Z))|(перв[уао][юяйи])',
	u'((\s|\A)2(\s|\Z))|(втор[уао][юяйи])',
	u'((\s|\A)3(\s|\Z))|(треть[юяейи]{1,2})',
	u'((\s|\A)4(\s|\Z))|(четверт[уао][юяйи])',
	u'((\s|\A)5(\s|\Z))|(пят[уао][юяйи])',
	u'((\s|\A)6(\s|\Z))|(шест[уао][юяйи])',
	u'((\s|\A)7(\s|\Z))|(седьм[уао][юяйи])'
]

LECTION_TIME = {
	1: '9:00-10:35',
	2: '10:45-12:20',
	3: '12:50-14:25',
	4: '14:35-16:10',
	5: '16:20-17:55',
	6: '18:00-19:35',
	7: '19:45-21:20'
}

# Keywords using when send message from group's chat.
CHAT_KEYWORDS = (
	u'расписание',
	u'бот'
)

# Keywords regexp for every command. Order is important!
CMD_KEYWORDS = {		
	CMD_FEEDBACK		: [
		u'разработчику', 
		u'предложение', 
		u'ошибка',
	],
	CMD_TOMMOROW		: [u'\sзавтра'],
	CMD_NEXT 			: [u'дальше', u'следующ[аи][яе]',  u'оставш[аи][яи]ся',  u'остал[аи]сь'],
	CMD_TODAY 			: [u'сегодня', u'^\s*расписание$', u'^\s*пар[аы]$'],
	CMD_AFTERTOMMOROW 	: [u'послезавтра'], 
	CMD_YESTERDAY		: [u'вчера'],
	CMD_WEEK			: [u'неделя'],
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
	CMD_POLITE			: [u'спас', u'спс'],
	CMD_TEACHER			: [u'кто', u'лектор', u'преподаватель', u'учитель', u'ведет'],
	CMD_LECTIONS_TIME	: [u'время', u'во\s?сколько', 'звонк'],
	CMD_WHEN_EXAMS		: [
		u'осталось',
		u'прошло[^й]', 
		u'пройден',
		u'семестр',
		u'сколько',
		u'когда',
		u'каникул'],
	CMD_BY_TIME			: ['(([01]?\d|2[0-3]):([0-5]\d)|24:00)'],
	CMD_BY_DATE			: ['(\d{1,2}\.\d{2})|(\d{1,2}\s*((' + ")|(".join(MONTH_NAMES) + ')))'],
	CMD_MAP				: [u'[абвгдАБВГД]\-?[1-9][0-9абвгдм\-]{0,4}'],
	CMD_ZACHET			: [u'зач[её]т'],
	CMD_EXAMS			: [u'экзамен'],
	CMD_CONSULT			: [u'консул'],
	CMD_SESSION			: [u'сесси[яи]'],
	CMD_CALENDAR_JN		: [u'календар.*январ'],
	CMD_CALENDAR_DC		: [u'календар.*декабр'],
	CMD_MYGROUP			: [u'запомн',u'сохран'],
	#CMD_WHERE			: [u'где', u'покажи'],
	CMD_LECTION_NUMB	: NUMB_NAMES,
}

USER_PREMESSAGE = {
	CMD_UNIVERSAL		: u'(для расписания сессии спросите про зачеты/экзамены)\nПары{markers}:\n',

	CMD_NOW				: u' сейчас',
	CMD_TODAY			: u' сегодня',
	CMD_TOMMOROW		: u' завтра',
	CMD_YESTERDAY		: u' вчера',
	CMD_AFTERTOMMOROW 	: u' послезавтра',
	CMD_DAY_OF_WEEK 	: u' в {}',
	CMD_BY_DATE			: u' {}',
	CMD_BY_TIME			: u' в {}',
	CMD_LECTION_NUMB	: u' номер {}',

	CMD_WEEK			: '',
	CMD_NEXT 			: u'Следующие пары:\n',
	CMD_LECTIONS_TIME	: u'Время начала-конца пар\n\n',
	CMD_FEEDBACK		: u'Сообщение принято и обязательно будет рассмотрено. Спасибо :)',
	CMD_HELP			: u'Краткая инструкция:\nПросто спросите что-нибудь по расписанию. '\
		+ u'Если на ваш вопрос нет ответа, то попробуйте написать по-другому, со временем бот '\
		+ u'научится отвечать на любые формы вопросов. '\
		+ u'В групповых беседах надо обращаться "раписание, ..."\n'\
		+ u'Полная инструкция есть на странице бота.\n\n'
		+ u'Во избежании блокировки есть ограничения:\n'\
		+ u'- бот отвечает только на понятные ему сообщения.\n'\
		+ u'- бот НЕ ПИШЕТ один и тот же ответ больше ОДНОГО раза.\n'\
		+ u'\nПримеры:\n'\
		+ u'"Какие пары завтра?"\n"Где аудитория Г-301д?"\n"Пары во вторник"\n"Расписание экзаменов"\n\n',
	CMD_POLITE			: u'Пожалуйста, обращайся ещё :)',
	CMD_SAVE_GROUP		: u'Я запомнил группу {}.\n\n',
	CMD_TEACHER			: u'Преподаватель на паре{markers}:\n',
	CMD_WHEN_EXAMS		: u'Зачетная неделя с 22 декабря.\nЭкзамены с 9 по 30 января.\n'\
		+ u'Каникулы с 31 января по 5 февраля.\n\n',
	CMD_FIND_LECTION	: u'',
	CMD_MAP				: u'',	
	CMD_ZACHET			: u'Зачеты.',
	CMD_EXAMS			: u'Экзамены.\n',
	CMD_CONSULT			: u'Консультации.\n',
	CMD_SESSION			: u'Расписание экзаменационной сессии.\n',
	CMD_CALENDAR_JN		: u'Календарь на январь',
	CMD_CALENDAR_DC		: u'Календарь на декабрь',
	CMD_MYGROUP			: u'',
	CMD_WHERE			: u'',
}

USER_MESSAGE = {
	CMD_UNIVERSAL		: u'\n{} пара ({}, {}):\n{}\n',
	CMD_WEEK			: u'{} неделя.',	
	CMD_LECTIONS_TIME	: u'{} пара: {}\n',
	CMD_WHEN_EXAMS		: u'Осталось недель: 0, дней: 0.\nСеместр завершен на 100%.',
	#CMD_WHEN_EXAMS		: u'Осталось недель: {}, дней: {}.\nСеместр завершен на {}.',
	CMD_MAP				: u'{}',
	CMD_EXAMS			: u'\n{} января в {}, {}:\n{}\n',
	CMD_CONSULT			: u'\n{} января в {}, {}:\n{}\n',
	CMD_SESSION			: u'\n{} января в {}, {}:\n{} "{}"\n',
	CMD_ZACHET			: u'\n{} пара{}\n{}\n',
	CMD_WHERE			: u'Аудитория {} ({})\n {}',
}

# Error codes, will raise as exceptions.
ERR_UNDEFINED 		= 0
ERR_SKIP			= 1
ERR_GROUP_NOT_FOUND = 2
ERR_NO_GROUP		= 3
ERR_NO_COMMAND		= 4
ERR_NO_LECTIONS		= 5
ERR_NO_TEACHER		= 6
ERR_NO_ROOM			= 7
ERR_PERIOD_ENDS		= 8
	
ERR_MESSAGES = {
	ERR_UNDEFINED		: u'Что-то пошло не так, повторите запрос еще раз.',
	ERR_SKIP			: '',
	ERR_GROUP_NOT_FOUND	: u'Группа не найдена.\nРасписание для данной группы недоступно,'\
		+ u' либо название группы указано с ошибками,.',
	ERR_NO_GROUP		: u'Напишите из какой вы группы.\nОбразец: расписание, ИКБО-04-15',
	ERR_NO_COMMAND		: u'Неизвестная команда.',
	ERR_NO_LECTIONS		: u'занятий нет',
	ERR_NO_TEACHER		: u'В расписании преподаватель не указан.',
	ERR_NO_ROOM			: u'Аудитория не найдена',
	ERR_PERIOD_ENDS		: u'занятий нет, смотрите расписание зачетов/экзаменов.'
}

MAP_DATA = [
	{
		'vk_id'	: '456239038',
		'name'	: 'A-1-left-end',
		'nam_ru': u'а',
		'rooms'	: u'178, 179, 180, 181, 182, 184а, 183, 184, 185, 186, 187, 188',
		'desc'	: u'Корпус А, 1 этаж.\nСпускаться по лестнице за аудиторией А-8.'
	},
	{
		'vk_id'	: '456239039',
		'name'	: 'A-1-left-middle-left',
		'nam_ru': u'а',
		'rooms'	: u'173, 174а, 174б, 190а, 175, 176, 177, 1771, 189, 190, 191, 192, 194, 195, 196, 197, 198, 199',
		'desc'	: u'Корпус А, 1 этаж.\nСпускаться по лестнице за аудиторией А-6.'
	},
	{
		'vk_id'	: '456239040',
		'name'	: 'A-1-left-middle-right',
		'nam_ru': u'а',
		'rooms'	: u'129, 131, 135, 137, 172, 171, 170, 168, 166, 164, 162, 160, 158, 156',
		'desc'	: u'Корпус А, 1 этаж.\nСпускаться по главной лестнице.'
	},
	{
		'vk_id'	: '456239041',
		'name'	: 'A-1-right-middle-right',
		'nam_ru': u'а',
		'rooms'	: u'1071, 107, 109, 111, 113, 115, 138, 136, 134, 132, 130, 128, 126, 124',
		'desc'	: u'Корпус А, 1 этаж.\nСпускаться по лестнице за аудиторией А-3.'
	},
	{
		'vk_id'	: '456239042',
		'name'	: 'A-2-left-end',
		'nam_ru': u'а',
		'rooms'	: u'223, 219, 220, 221, 222, 223, 224, 225, 226, 227,228, 229, 2301,2302,231,232, 235',
		'desc'	: u'Корпус А, 2 этаж.\nНалево от главной лестницы и до конца.'
	},
	{
		'vk_id'	: '456239055',
		'name'	: 'A-2-left-middle',
		'nam_ru': u'а',
		'rooms'	: u'218, 8, 217, 7, 217, 7, 216, 6, 215, 5, 214, 2142,2141',
		'desc'	: u'Корпус А, 2 этаж.\nНалево от главной лестницы.'
	},
	{
		'vk_id'	: '456239044',
		'name'	: 'A-2-right-end',
		'nam_ru': u'а',
		'rooms'	: u'208,207,206,205,204,203',
		'desc'	: u'Корпус А, 2 этаж.\nНаправо от главной лестницы и до конца.'
	},
	{
		'vk_id'	: '456239056',
		'name'	: 'A-2-right-middle',
		'nam_ru': u'а',
		'rooms'	: u'213,2132,2131,212,4,211,3,210,2,209,1',
		'desc'	: u'Корпус А, 2 этаж.\nНаправо от главной лестницы.'
	},
	{
		'vk_id'	: '456239046',
		'name'	: 'A-3-left-end',
		'nam_ru': u'а',
		'rooms'	: u'325,326,327,328,329,3301,330,331,332,333,334,335,336',
		'desc'	: u'Корпус А, 3 этаж.\nПодниматься по лестнице за аудиторией А-8.'
	},
	{
		'vk_id'	: '456239057',
		'name'	: 'A-3-left-middle',
		'nam_ru': u'а',
		'rooms'	: u'324,18,17,323,322,16,15,321,320,14,319',
		'desc'	: u'Корпус А, 3 этаж.\nПодниматься по главной лестнице, потом налево.'
	},
	{
		'vk_id'	: '456239058',
		'name'	: 'A-3-right-middle',
		'nam_ru': u'а',
		'rooms'	: u'318,13,317,316,12,11,315,314,10,9,313',
		'desc'	: u'Корпус А, 3 этаж.\nПодниматься по главной лестнице, потом направо.'
	},
	{
		'vk_id'	: '456239024',
		'name'	: 'A-3-right-end',
		'nam_ru': u'а',
		'rooms'	: u'301,303,305,307,309,311,312,310,308,306,304,302,300',
		'desc'	: u'Корпус А, 3 этаж.\nПодниматься по лестнице за аудиторией А-1'
	},
	{
		'vk_id'	: '456239059',
		'name'	: 'A-4-left-end',
		'nam_ru': u'а',
		'rooms'	: u'18а,425,427,429,438,436,434,433,430,428,426',
		'desc'	: u'Корпус А, 4 этаж.\nПодниматься по лестнице за аудиторией А-8.'
	},
	{
		'vk_id'	: '456239060',
		'name'	: 'A-4-middle',
		'nam_ru': u'а',
		'rooms'	: u'423,426,422,420,420а,419,439,418,417,416',
		'desc'	: u'Корпус А, 4 этаж.\nПодниматься по главной лестнице, потом в дверь посередине.'
	},
	{
		'vk_id'	: '456239051',
		'name'	: 'A-4-right-end',
		'nam_ru': u'а',
		'rooms'	: u'401,403,405,407,409,411,9а,412,410,408,406,404,402',
		'desc'	: u'Корпус А, 4 этаж.\nПодниматься по лестнице за аудиторией А-1.'
	},
	{
		'vk_id'	: '456239065',
		'name'	: 'G-1',
		'nam_ru': u'г1',
		'rooms'	: '',
		'desc'	: u'Корпус Г, 1 этаж.'
	},
	{
		'vk_id'	: '456239032',
		'name'	: 'G-2',
		'nam_ru': u'г2',
		'rooms'	: '',
		'desc'	: u'Корпус Г, 2 этаж.'
	},
	{
		'vk_id'	: '456239064',
		'name'	: 'G-3',
		'nam_ru': u'г3',
		'rooms'	: '',
		'desc'	: u'Корпус Г, 3 этаж.'
	},
	{
		'vk_id'	: '456239034',
		'name'	: 'G-4',
		'nam_ru': u'г4',
		'rooms'	: '',
		'desc'	: u'Корпус Г, 4 этаж.'
	},
	{
		'vk_id'	: '456239035',
		'name'	: 'V-2',
		'nam_ru': u'в2',
		'rooms'	: '',
		'desc'	: u'Корпус В, 2 этаж.'
	},
	{
		'vk_id'	: '456239036',
		'name'	: 'V-3',
		'nam_ru': u'в3',
		'rooms'	: '',
		'desc'	: u'Корпус В, 3 этаж.'
	},
	{
		'vk_id'	: '456239037',
		'name'	: 'V-4',
		'nam_ru': u'в4',
		'rooms'	: '',
		'desc'	: u'Корпус В, 4 этаж.'
	},
	{
		'vk_id'	: '456239025',
		'name'	: 'B-1',
		'nam_ru': u'б1',
		'rooms'	: '',
		'desc'	: u'Корпус Б, 1 этаж.'
	},
	{
		'vk_id'	: '456239026',
		'name'	: 'B-2',
		'nam_ru': u'б2',
		'rooms'	: '',
		'desc'	: u'Корпус Б, 2 этаж.'
	},
	{
		'vk_id'	: '456239027',
		'name'	: 'B-3',
		'nam_ru': u'б3',
		'rooms'	: '',
		'desc'	: u'Корпус Б, 3 этаж.'
	},
	{
		'vk_id'	: '456239028',
		'name'	: 'B-4',
		'nam_ru': u'б4',
		'rooms'	: '',
		'desc'	: u'Корпус Б, 4 этаж.'
	},
	{
		'vk_id'	: '456239029',
		'name'	: 'D-2',
		'nam_ru': u'д2',
		'rooms'	: '',
		'desc'	: u'Корпус Д, 2 этаж.'
	},
	{
		'vk_id'	: '456239030',
		'name'	: 'D-3',
		'nam_ru': u'д3',
		'rooms'	: '',
		'desc'	: u'Корпус Д, 3 этаж.'
	},
]

