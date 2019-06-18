#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class GroupException(Exception):
    def __init__(self, message, suggestion):
        super(GroupException, self).__init__(message)
        self.suggestion = suggestion


STACK_LEN = 500  # messages
USERS_QUEUE_LEN = 600  # seconds
USER_MSG_AMOUNT = 1  # message amount for a user in USERS_QUEUE_LEN
NOTICE_START_HOUR = 3  # Hour when notice delivery starts
NOTICE_END_HOUR = 6  # Hour when notice delivery ends
NOTICE_DELAY = 20  # Seconds while waiting for next notice

LOG = True  # Enable/disable logging everything.
LOG_DIR = 'log/'  # Logs directory.

# Log type codes
LOG_ERROR = 10  # Errors / exceptions
LOG_WLOAD = 20  # Bot workload
LOG_FBACK = 30  # Feedback
LOG_MESGS = 40  # Any message
LOG_STATS = 50  # Statistics

# Log file names
LOG_ERROR_FILE = 'exceptions.txt'
LOG_WLOAD_FILE = 'workload.txt'
LOG_FBACK_FILE = 'feedback.txt'
LOG_MESGS_FILE = 'messages.txt'
LOG_PARSE_FILE = 'parser.txt'
LOG_STATC_FILE = 'statistic.txt'

SCHEDULE_DIR = 'schedules/'  # Directory with schedule documents

# Commands (CMD) codes
CMD_AFTERTOMMOROW = 10010
CMD_TOMMOROW = 10020
CMD_YESTERDAY = 10030
CMD_DAY_OF_WEEK = 10040
CMD_BY_DATE = 10050
CMD_BY_TIME = 10060
CMD_BY_NUMB = 10070
CMD_TODAY = 10080
CMD_NOW = 10090
CMD_NEXT = 10100
CMD_FIRST = 10110

# Command code uses as command priority number.
# Command with lower code has higher priority.
CMD_LESSONS = 990  # base command for showing lessons
CMD_HOT_FUNC = 190
CMD_WEEK = 200  # get semester's week number from date
CMD_HELP = 210
CMD_POLITE = 220
CMD_LESSONS_TIME = 230
CMD_MY_TEACHERS = 235
CMD_TEACHER = 240  # get teacher's name for lesson
CMD_LESSONS_COUNTER = 255  # rest of lessons in semester
CMD_WHEN_EXAMS = 260
CMD_FEEDBACK = 270  # message to developer
CMD_MYGROUP = 290
CMD_SAVE_GROUP = 300
CMD_MAP = 310  # search room on the map
CMD_EXAMS = 320
CMD_CONSULT = 330
CMD_SESSION = 340
CMD_ZACHET = 370
CMD_WHERE_LESSON = 380  # search lesson's room on the map
CMD_FOR7DAYS = 390  # lesson for several days (7 - default)
CMD_JUST_LESSONS = 400  # if no any other words in the message
CMD_NEW_ID = 410  # new web page ID
CMD_MYID = 420
CMD_LINK = 430
CMD_SEARCH_TEACHER = 440
CMD_NOTICE = 450
CMD_CHANGES = 460
CMD_PIDR = 470

# Time markers. Could be with base command.
MARKERS = [
    CMD_NOW,
    CMD_NEXT,
    CMD_TODAY,
    CMD_TOMMOROW,
    CMD_AFTERTOMMOROW,
    CMD_YESTERDAY,
    CMD_DAY_OF_WEEK,
    CMD_BY_NUMB,
    CMD_BY_TIME,
    CMD_BY_DATE,
    CMD_FIRST
]

DAY_NAMES = [
    u'понедельник',
    u'вторник',
    u'среда',
    u'четверг',
    u'пятница',
    u'суббота',
    u'воскресение',
]

DAY_NAMES_SHORT = [
    u'пн',
    u'вт',
    u'ср',
    u'чт',
    u'пт',
    u'сб',
    u'вс',
]

DAY_NAMES_VINIT = [
    u'понедельник',
    u'вторник',
    u'среду',
    u'четверг',
    u'пятницу',
    u'субботу',
    u'воскресение',
]

MONTH_NAMES = [
    u'январ[яь]',
    u'феврал[яь]',
    u'мартa?',
    u'апрел[яь]',
    u'ма[йя]?',
    u'июн[яь]',
    u'июл[яь]',
    u'августа?',
    u'сентябр[яь]',
    u'октябр[яь]',
    u'ноябр[яь]',
    u'декабр[яь]',
]

MONTH_NAMES_RODIT = [
    u'января',
    u'февраля',
    u'мартa',
    u'апреля',
    u'мая',
    u'июня',
    u'июля',
    u'августа',
    u'сентября',
    u'октября',
    u'ноября',
    u'декабря',
]

NUMB_NAMES = [
    u'((\s|\A)0(\s|\Z))|(нулевая)',
    u'(\s|\A)1(\s|\Z)',
    u'((\s|\A)2(\s|\Z))|(втор[уаоы][еюяйи])',
    u'((\s|\A)3(\s|\Z))|(треть[юяейи]{1,2})',
    u'((\s|\A)4(\s|\Z))|(четверт[уаоы][еюяйи])',
    u'((\s|\A)5(\s|\Z))|(пят[уаоы][еюяйи])',
    u'((\s|\A)6(\s|\Z))|(шест[уаоы][еюяйи])',
    u'((\s|\A)7(\s|\Z))|(седьм[уаоы][еюяйи])'
]

LECTION_TIME = {
    1: '9:00-10:30',
    2: '10:40-12:10',
    3: '13:00-14:30',
    4: '14:40-16:10',
    5: '16:20-17:50',
    6: '18:00-19:30',
    7: '18:30-20:00',
    8: '20:10-21:40',
}

# Keywords using when get message from group's chat.
CHAT_KEYWORDS = (
    u'расписание',
    u'бот'
)

FEEDBACK_KEYWORDS = (
    u'разработчик',
    u'предложен',
    u'ошибк',
)

# Keywords regexp to define every command.
KEYWORDS = {
    CMD_TOMMOROW: [u'(\s|\A)завтра'],
    CMD_NEXT: [u'будет', u'дальше', u'следующ[аи][яе]', u'оставш[аи][яи]ся',
               u'остал[аи]сь'],
    CMD_TODAY: [u'сегодня'],
    CMD_AFTERTOMMOROW: [u'послезавтра'],
    CMD_YESTERDAY: [u'вчера'],
    CMD_WEEK: [u'неделя', u'номер.*недел'],
    CMD_NOW: [u'сейчас', u'текущая'],
    CMD_FIRST: [u'перв[уаоы][еяюйи]'],
    CMD_DAY_OF_WEEK: [
         u'((\s|\A)пн(\s|\Z))|(понедельник)',
         u'((\s|\A)вт(\s|\Z))|(вторник)',
         u'((\s|\A)ср(\s|\Z))|(сред[ау])',
         u'((\s|\A)чт(\s|\Z))|(четверг)',
         u'((\s|\A)пт(\s|\Z))|(пятниц[ау])',
         u'((\s|\A)сб(\s|\Z))|(суббот[ау])',
         u'((\s|\A)вс(\s|\Z))|(воскресение)'
     ],
    CMD_HELP: [
        u'инструкци',
        u'справка',
        u'помощь',
        u'help',
        u'работаешь',
        u'пользоваться',
        u'умее',
        u'делаешь',
        u'команды',
        u'глупый'
    ],
    CMD_POLITE: [u'спас', u'спс', u'благордар'],
    CMD_MY_TEACHERS: [u'преподавател', u'учителя', u'преподы',
                       u'список'],
    CMD_TEACHER: [u'кто', u'лектор', u'препод', u'учитель', u'ведет'],
    CMD_LESSONS_TIME: [u'время', u'во\s?сколько', u'звонк'],
    CMD_LESSONS_COUNTER: [
        u'сч[её]тчик',
        u'((сколько)|(осталось)|(кол(ичест)|(-)во)|(список)).*'
        + u'((пар)|(занятий))',
        u'((пар)|(занятий)).*((сколько)|(осталось)|'
        + u'(кол(ичест)|(-)во)|(список))',
    ],
    CMD_WHEN_EXAMS: [
        u'осталось',
        u'прошло[^й]?',
        u'пройден',
        u'семестр',
        u'сколько',
        u'когда',
        #u'каникул',
        u'зачет',
        u'экзамен',
        u'сессия',
    ],
    CMD_BY_TIME: ['(([01]?\d|2[0-3]):([0-5]\d)|24:00)'],
    CMD_BY_DATE: ['(\d{1,2}\.\d{2})|(\d{1,2}\s*((' + ")|(".join(
        MONTH_NAMES) + ')))'],
    CMD_MAP: [u'[Aaа-я]\-?[1-9][0-9Aaа-я\-]{0,4}'],
    CMD_MYGROUP: [u'запомн', u'сохран', u'групп'],
    CMD_WHERE_LESSON: [u'где', u'покажи'],
    CMD_BY_NUMB: NUMB_NAMES,
    CMD_FOR7DAYS: [u'недел[юе]', u'[1-7]\s*дн[ея]'],
    CMD_JUST_LESSONS: [u'(\s|\A)расписание\Z', u'(\s|\A)пары\Z'],
    CMD_NEW_ID: [u'новый', u'генерир', u'обнови'],
    CMD_MYID: [u'id', u'логин', u'пароль'],
    CMD_LINK: [u'ссылка', u'адрес', u'страница', u'сайт'],
    CMD_HOT_FUNC: [u'\A[1-4]\Z'],
    CMD_SEARCH_TEACHER: [
        u'[а-я]+\s[а-я]\.\s?[а-я]\.',
        u'най[тд]и\s[а-я]*(\s[а-я]\.?\s?[а-я]\.?)?(\s|\Z)'],
    CMD_NOTICE: [u'уведомлен', u'напомин', u'🔔'],
    CMD_CHANGES: [u'обновлен', u'изменен', u'истори'],
    CMD_PIDR: [u'пидр']
}

# Some text, which automatically enters before answer body.
USER_PREMESSAGE = {
    CMD_LESSONS: u'Пары{markers}:\n',

    CMD_NOW: u' сейчас',
    CMD_TODAY: u' сегодня',
    CMD_TOMMOROW: u' завтра',
    CMD_YESTERDAY: u' вчера',
    CMD_AFTERTOMMOROW: u' послезавтра',
    CMD_DAY_OF_WEEK: u' на {}',
    CMD_BY_DATE: u' {}',
    CMD_BY_TIME: u' в {}',
    CMD_BY_NUMB: u' номер {}',
    CMD_FIRST: u' (первая)',

    CMD_WEEK: '',
    CMD_NEXT: u' следующая',
    CMD_LESSONS_TIME: u'# пара: начало-конец\n\n',
    CMD_FEEDBACK: u'Сообщение принято. Спасибо :)',
    CMD_HELP: u'',
    CMD_POLITE: u'Пожалуйста, обращайся ещё :)',
    CMD_SAVE_GROUP: u'Я запомнил группу {}.\n\n',
    CMD_TEACHER: u'Преподаватель на паре{markers}:\n',
    CMD_LESSONS_COUNTER: u'Осталось пар до ',
    CMD_WHEN_EXAMS: u'',
    CMD_MAP: u'',
    CMD_ZACHET: u'Зачеты.',
    CMD_EXAMS: u'Экзамены.\n',
    CMD_CONSULT: u'Консультации.\n',
    CMD_SESSION: u'Расписание экзаменационной сессии.\n',
    CMD_MYGROUP: u'',
    CMD_WHERE_LESSON: u'',
    CMD_FOR7DAYS: u'',
    CMD_JUST_LESSONS: u'Пары {markers}:\n',
    CMD_NEW_ID: u'Ссылка: botpage.ru \n',
    CMD_MYID: u'Ссылка: botpage.ru \n',
    CMD_LINK: u'',
    CMD_SEARCH_TEACHER: u'',
    CMD_MY_TEACHERS: u'Список преподавателей:\n\n',
    CMD_NOTICE: u'',
    CMD_CHANGES: u'История изменений расписания:\n',
    CMD_PIDR: u''
}

# Templates for command's body text.
USER_MESSAGE = {
    CMD_LESSONS: u'\n{} пара ({}{}):\n{}\n',
    CMD_WEEK: u'{} неделя.',
    CMD_LESSONS_TIME: u'{} пара: {}\n',
    CMD_LESSONS_COUNTER: u'{} - {} {}\n',
    CMD_WHEN_EXAMS: u'До сессии осталось недель: {}, дней: {}.'
                    + u'\nСеместр пройден на {}%.',
    CMD_MAP: u'{}',
    CMD_EXAMS: u'\n{} января в {}, {}:\n{}\n',
    CMD_CONSULT: u'\n{} января в {}, {}:\n{}\n',
    CMD_SESSION: u'\n{} января в {}, {}:\n{} "{}"\n',
    CMD_ZACHET: u'\n{} пара{}\n{}\n',
    CMD_WHERE_LESSON: u'Аудитория {} ({}){}\n',
    CMD_FIRST: u' ({} пара)',
    CMD_HELP: u'Бот дополнительно может:\n'
        + u'- найти преподавателя "найди антика"\n'
        + u'- показать пары по дате и времени "пара 31.12 в 16:30"\n'
        + u'- показать пары дням (не больше 7 дней) "3 пары на 5 дней"\n'
        + u'- показать аудиторию "где а-9а" (только для МИРЭА)\n'
        + u'- уведомлять о парах "уведомления"\n'
        + u'- посчитать оставшиеся пары "счетчик"\n'
        + u'- сообщить номер недели\n\n'
        + u'Бот не несет ответственности за пропуски пар.',
    CMD_NEW_ID: u'Ваш новый ID: {}',
    CMD_MYID: u'Ваш ID: {}',
    CMD_SEARCH_TEACHER: u'{} пара в {} (групп {})\n{}\n\n',
    CMD_MY_TEACHERS: u'{}\n{}\n\n',
    CMD_LINK: u'botpage.ru',
    CMD_NOTICE: u'Уведомления {}.\n\nПо умолчанию включаются "пары на день" и "схема с первой парой", но '
        + u'это можно изменить на botpage.ru/editor.',
    CMD_CHANGES: u'_________\n{}\n{}\n\n{}\n\n',
}

USER_POSTMESSAGES = {
    CMD_MY_TEACHERS: u'Для {} пар преподаватель не написан.',
    CMD_LESSONS_COUNTER: u'\n* без учета праздничных дней *',
}

# Default notice message text.
MSG_NOTICE_TODAY = u'бот, пары сегодня'
MSG_NOTICE_TOMORROW = u'бот, пары завтра'
MSG_NOTICE_WEEK = u'бот, на неделю'
MSG_NOTICE_MAP = u'бот, где первая пара'
MSG_ZERO_HOUR = u'\n\nУже {}!'

# Error codes, will raise as exceptions.
ERR_UNDEFINED = 0
ERR_SKIP = 1
ERR_GROUP_NOT_FOUND = 2
ERR_NO_GROUP = 3
ERR_NO_COMMAND = 4
ERR_NO_LECTIONS = 5
ERR_NO_TEACHER = 6
ERR_NO_ROOM = 7
ERR_PERIOD_ENDS = 8
ERR_MSG_LIMIT = 9
ERR_NO_TEACHER_FOUND = 10
ERR_DUMMY = 11

ERR_MESSAGES = {
    ERR_UNDEFINED: u'Что-то пошло не так, повторите запрос еще раз.\n'
                    + u'Если сообщение повторяется, напишите на '
                    + u'timetable.bot@yandex.ru',
    ERR_SKIP: '',
    ERR_GROUP_NOT_FOUND: u'Расписание для группы недоступно.\n'
                         + u'Возможно группа указана с ошибками '
                         + u'(образец: ИКБО-04-15).',
    ERR_NO_GROUP: u'Напишите из какой вы группы.\n'
                  + u'Образец: расписание, ИКБО-04-15\n\n'
                  + u'Не забудьте символ "-" и нули, если есть.',
    ERR_NO_COMMAND: u'Неизвестная команда.',
    ERR_NO_LECTIONS: u'по запросу пары не найдены',
    ERR_NO_TEACHER: u'В расписании преподаватель не указан.',
    ERR_NO_ROOM: u'Аудитория на схемах не найдена',
    ERR_PERIOD_ENDS: u'Семестр закончился, смотрите расписание '
                     + u'зачетов/экзаменов на '
                     + 'https://www.mirea.ru/education/schedule-main/schedule/',
    ERR_MSG_LIMIT: u'\n* пауза на {} сек. *',
    ERR_NO_TEACHER_FOUND: u'Расписание для преподавателя не найдено.',
    ERR_DUMMY: u"Кажется, сообщение с ошибками или не "
               u"относится к расписанию. "
}
