#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from operator import itemgetter
from random import randint
import datetime as dt
import re
import hashlib

import consts as CONST
import logger as LOGGER
import dbmodels as DB


def genBotID(any_string):
    """ Generates unique user ID for database.
    
    :param any_string: base string for hash generating
    :type any_string: str
    :return: bot_id for database
    :rtype: str
    """
    md5_hash = hashlib.md5()
    id_free = False
    new_hash = ''
    while not id_free:
        md5_hash.update(str(any_string) + str(randint(0, 10000)))
        new_hash = md5_hash.hexdigest()
        try:
            user = DB.Users.get(DB.Users.bot_id == new_hash)
        except:
            user = False
        if not user:
            id_free = True
    return new_hash


def getLessonNumb(dt_time):
    """ Defines lesson number for given time.
    
    :param dt_time: any time value
    :type dt_time: time
    :return: lesson number
    :rtype: int
    """

    # noinspection PyTypeChecker
    return {
        dt_time < dt.time(9, 0, 0): 0,
        dt.time(8, 0, 0) <= dt_time < dt.time(10, 30, 0): 1,
        dt.time(10, 30, 0) <= dt_time < dt.time(12, 10, 0): 2,
        dt.time(12, 10, 0) <= dt_time < dt.time(14, 30, 0): 3,
        dt.time(14, 30, 0) <= dt_time < dt.time(16, 10, 0): 4,
        dt.time(16, 10, 0) <= dt_time < dt.time(17, 50, 0): 5,
        dt.time(18, 00, 0) <= dt_time < dt.time(19, 30, 0): 6,
        dt.time(19, 30, 0) <= dt_time < dt.time(20, 00, 0): 7,
        dt.time(20, 00, 0) <= dt_time < dt.time(21, 40, 0): 8,
        dt.time(21, 40, 0) <= dt_time: 9
    }[True]


def isWeeksEqual(doc_week, cal_week):
    """ Compare 'week' value from schedule documents
    and calendar week number for equality.
    
    :param doc_week: 'week' value from schedule documents
    :type doc_week: str
    :param cal_week: calendar week number
    :type cal_week: int
    :return: is document's week value match calendar's week
    :rtype: bool
    """
    cal_week = cal_week - dt.date(2017, 2, 6).isocalendar()[1] + 1

    if doc_week == '':
        result = True
    elif 'I' in doc_week:
        result = (cal_week % 2 == 0) == (doc_week.strip() == 'II')
    elif '-' in doc_week:
        period = re.split('-', doc_week)
        result = (cal_week >= int(period[0])) and (
            cal_week <= int(period[1]))
    else:
        result = str(cal_week) in re.split(r'[\s,]', doc_week)
    return result


def findFloor(room_name):
    """ Search room on maps.
    
    :param room_name: room to find, could be in any format
    :type room_name: str
    :return: floor (global map's part)
    :rtype: dict
    """
    room_name = room_name.lower().replace('-', '')
    campus = room_name[:1]
    room_number = room_name[1:]

    found_floor = {}
    if campus == u'а':
        for floor in CONST.MAP_DATA:
            if floor['nam_ru'][:1] == campus:
                for map_room in floor['rooms'].split(','):
                    if room_number == map_room.replace(' ', ''):
                        found_floor = floor
    else:
        for floor in CONST.MAP_DATA:
            if floor['nam_ru'] == (campus + room_number[:1]):
                found_floor = floor

    return found_floor


def getFullSchedule(params):
    """ Retrieves official and user's schedule and merge it.
    
    :param params: needed in 'vk_id', 'is_chat', 'group'
    :type params: dict
    :return: user's full schedule
    :rtype: list
    """
    schedule_base = DB.Schedule.filter(group=params['group']['id'])
    try:
        db_user = DB.Users.get(
            DB.Users.vk_id == params['vk_id'],
            DB.Users.is_chat == params['is_chat']
        )
        schedule_user = DB.UsersSchedule.filter(user=db_user)
    except:
        schedule_user = []
    schedule = []
    for event_base in schedule_base:
        no_major = True
        for event_user in schedule_user:
            if event_user.week == event_base.week \
                    and event_user.day == event_base.day \
                    and event_user.numb == event_base.numb:
                no_major = False
                break
        if not no_major:
            continue
        event = {
            'name': event_base.name,
            'week': event_base.week,
            'day': event_base.day,
            'numb': event_base.numb,
            'teacher': event_base.teacher,
            'room': event_base.room,
        }
        schedule.append(event)
    for event_user in schedule_user:
        if event_user.hide:
            continue
        event = {
            'name': event_user.name,
            'week': event_user.week,
            'day': event_user.day,
            'numb': event_user.numb,
            'teacher': event_user.teacher,
            'room': event_user.room,
        }
        schedule.append(event)

    if not schedule:
        raise Exception(CONST.ERR_NO_LECTIONS)

    schedule = sorted(schedule, key=itemgetter('day', 'numb'))
    return schedule


def getLessons(params, les_first=1, les_last=8):
    """ Filter user's schedule using parameters.
    
    :param params: common command parameters
    :type params: dict
    :param les_first: first lesson number 
    :type les_first: int
    :param les_last: last lesson number
    :type les_last: int
    :return: lessons for one specified day
    :rtype: list
    """
    schedule = getFullSchedule(params)

    lessons = []
    for event in schedule:
        if event['day'] == params['day']\
                and les_first <= event['numb'] <= les_last\
                and isWeeksEqual(event['week'], params['week']):
            try:
                if params['find_first'] and lessons[-1]['day'] == \
                        event['day']:
                    continue
            except:
                pass

            event['time'] = CONST.LECTION_TIME[event['numb']]
            lessons.append(event)

    if not lessons:
        raise Exception(CONST.ERR_NO_LECTIONS)

    return lessons


def formatLessons(lesson_list):
    """ Converts lessons for human readable strings.
    
    :param lesson_list: list of lessons
    :type lesson_list: list
    :return: human readable lessons
    :rtype: str
    """
    string = ''
    for lesson in lesson_list:
        string += CONST.USER_MESSAGE[CONST.CMD_LESSONS].format(
            lesson['numb'],
            lesson['room'] + ', ' if lesson['room'] else '',
            lesson['time'],
            lesson['name']
        )

    return string


def cmdLessons(params):
    """ Perform basic bot function. Prepare lessons list using params. 
    
    :param params: lesson parameters
    :type params: dict
    :return: formatted for user lesson list
    :rtype: str 
    """
    if params['lnumb']:
        lnumb = params['lnumb']
        lesson_list = getLessons(params, lnumb, lnumb)
    else:
        lesson_list = getLessons(params)

    return formatLessons(lesson_list)


def cmdWeek(params):
    """ Define week number from the study time start for given date.
    
    :param params: needed in date parameter
    :type params: dict
    :return: formatted for user week number
    :rtype: str
    """
    weeks = (params['date'].date() - dt.date(2017, 2, 5)).days / 7 + 1

    return CONST.USER_MESSAGE[CONST.CMD_WEEK].format(weeks)


def cmdLessonsTime(params):
    """ Retrieves lessons begin and end time.
    
    :param params: no parameters needed, saved for common interface
    :type params: dict
    :return: lesson time for user
    :rtype: str
    """
    msg = ''
    for i in CONST.LECTION_TIME:
        msg += CONST.USER_MESSAGE[CONST.CMD_LESSONS_TIME]\
            .format(i, CONST.LECTION_TIME[i])

    return msg


def cmdTeacher(params):
    """ Get teacher name for specified lesson.
    
    :param params: lesson parameters
    :type params: dict
    :return: teacher's name
    :rtype: str
    """
    lesson = getLessons(params, params['lnumb'], params['lnumb'])[0]
    teacher = lesson.get('teacher', '')
    if not teacher:
        raise Exception(CONST.ERR_NO_TEACHER)

    return teacher


def cmdHelp(params):
    """ Currently gets vk wall post with instructions.
    
    :param params: no parameters needed, saved for common interface
    :type params: dict
    :return: blank string
    :rtype: str
    """
    global attachment
    attachment = 'wall385457066_127'

    return ''


def cmdPolite(params):
    """ Currently do nothing. Idea is to take some polite phrases.
    
    :param params: no parameters
    :type params: dict
    :return: blank string
    :rtype: str
    """

    return ''


def cmdLessonsCounter(params):
    """ Count rest amount for all lessons.
    
    :param params: need start date
    :type params: dict
    :return: formatted for user lesson's list with rest amount
    :rtype: str
    """
    schedule = getFullSchedule(params)

    ev_amount = {}
    for event in schedule:
        ev_amount[event['name']] = {'amount': 0, 'last_date': ''}

    date_iter = dt.datetime.now().date()
    try:
        end = params['date'].date()
    except:
        end = params['date']
    if date_iter >= end:
        end = dt.date(2017, 5, 29)
    while date_iter != end:
        day = date_iter.weekday()
        week = date_iter.isocalendar()[1]
        month_name = CONST.MONTH_NAMES_RODIT[date_iter.month - 1]
        date_name = u'({} {})'.format(date_iter.day, month_name)
        for event in schedule:
            if event['day'] == day \
                    and isWeeksEqual(event['week'], week):
                ev_amount[event['name']]['amount'] += 1
                ev_amount[event['name']]['last_date'] = date_name
        date_iter = date_iter + + dt.timedelta(days=1)

    month_name = CONST.MONTH_NAMES_RODIT[end.month - 1]
    answer = u'{} {}:\n\n'.format(end.day, month_name)
    for name in sorted(ev_amount):
        last_date = ''
        if ev_amount[name]['amount'] == 1:
            last_date = ev_amount[name]['last_date']
        answer += CONST.USER_MESSAGE[CONST.CMD_LESSONS_COUNTER] \
            .format(name, ev_amount[name]['amount'], last_date)

    answer += CONST.USER_POSTMESSAGES[CONST.CMD_LESSONS_COUNTER]

    return answer


def cmdWhenExams(params):
    """ Calculate some statistic for session time.
    
    :param params: no parameters need, save for common interface
    :type params: dict
    :return: formatted for user statistic
    :rtype: str
    """
    now = dt.datetime.now().date()
    start = dt.date(2017, 2, 6)
    end = dt.date(2017, 5, 29)
    delta = end - now
    weeks = delta.days / 7
    days = delta.days % 7

    delta = now - start
    amount = end - start
    percent = str(
        int(round((float(delta.days) / amount.days) * 100))) + '%'

    global attachment
    attachment = 'wall385457066_137'

    return CONST.USER_MESSAGE[CONST.CMD_WHEN_EXAMS].format(weeks,
                                                           days,
                                                           percent)


def cmdMap(params):
    """ Searches room on map. Attach scheme to message.
    
    :param params: need user keyword 
    :type params: dict
    :return: formatted for user room location
    :rtype: str
    """
    global attachment

    floor = findFloor(params['keyword']['word'])

    if floor:
        attachment = 'photo385457066_' + floor['vk_id']
    else:
        raise Exception(CONST.ERR_NO_ROOM)

    return CONST.USER_MESSAGE[CONST.CMD_MAP].format(floor['desc'])


def cmdMyGroup(params):
    """ Format user group code for human readable string.
    
    :param params: needed in user group
    :type params: dict
    :return: user group code
    :rtype: str
    """
    return params['group']['code'].upper()


# noinspection PyTypeChecker
def cmdWhereLesson(params):
    """ Searches lesson and shows it's room on a map.
    
    :param params: needed in lesson date and time 
    :type params: dict
    :return: formatted for user lesson location
    :rtype: str
    """
    global attachment

    lesson_numb = ''
    if params['find_first']:
        lesson = getLessons(params)[0]
        lesson_numb = CONST.USER_MESSAGE[CONST.CMD_FIRST].format(
            lesson['numb'])
    else:
        lnumb = params['lnumb'] if params['lnumb'] else int(
            getLessonNumb(dt.datetime.now().time()))
        lesson = getLessons(params, lnumb, lnumb)[0]

    if not lesson.get('room', False):
        raise Exception(CONST.ERR_NO_ROOM)

    text = CONST.USER_MESSAGE[CONST.CMD_WHERE_LESSON].format(
        lesson['room'].upper(),
        lesson['name'],
        lesson_numb
    )

    floor = findFloor(lesson['room'])
    if floor:
        attachment = 'photo385457066_' + floor['vk_id']
    else:
        text += CONST.ERR_MESSAGES[CONST.ERR_NO_ROOM]

    return text


def cmdFor7Days(params):
    """ Combine lessons for several day forward.
    
    :param params: needed in a date and days amount
    :type params: dict
    :return: grouped by days list of lessons
    :rtype: str
    """
    day_amount = 7
    try:
        day_amount = int(
            re.search('[1-7]', params['keyword']['word']).group())
    except:
        pass

    text = ''
    for i in range(0, day_amount):
        date = params['date'] + dt.timedelta(days=i)
        weekday = date.weekday()

        params['day'] = weekday
        params['week'] = date.isocalendar()[1]
        try:
            if params['lnumb']:
                lesson_list = getLessons(params, params['lnumb'],
                                         params['lnumb'])
            else:
                lesson_list = getLessons(params)
        except:
            continue

        if weekday == 6:
            continue

        if len(lesson_list) == 0:
            continue

        dname = CONST.DAY_NAMES[weekday].title()
        text += '_' * (len(dname) + len(
            dname) / 2 + 6) + '\n' + dname + ' ' + date.strftime(
            '%d.%m') + '\n'
        text += formatLessons(lesson_list)
        text += '\n'

    if len(text) == 0:
        raise Exception(CONST.ERR_NO_LECTIONS)

    return text


def cmdNewId(params):
    """ Generates new bot id for user.
    
    :param params: needed in user properties
    :type params: dict
    :return: formatted for user new ID
    :rtype: str
    """
    new_hash = genBotID(params['vk_id'])
    user = DB.Users.get(
        DB.Users.vk_id == params['vk_id'],
        DB.Users.is_chat == params['is_chat']
    )
    user.bot_id = new_hash
    user.save()
    return CONST.USER_MESSAGE[CONST.CMD_NEW_ID].format(new_hash)


def cmdMyid(params):
    """ Retrieves user id.
    
    :param params: needed in user properties
    :type params: dict
    :return: formatted for user user ID
    :rtype: str
    """
    user = DB.Users.get(
        DB.Users.vk_id == params['vk_id'],
        DB.Users.is_chat == params['is_chat']
    )
    return CONST.USER_MESSAGE[CONST.CMD_MYID].format(user.bot_id)


def cmdLink(params):
    """ Retrieves bot's web page url.
    
    :param params: need nothing, saved for common interface
    :type params: dict
    :return: web page url
    :rtype: str
    """

    return CONST.USER_MESSAGE[CONST.CMD_LINK]


def cmdSearchTeacher(params):
    """ Searches nearest teacher's lessons. 
    
    :param params: needed in teacher name and starting date
    :type params: dict
    :return: formatted for user list of teacher's lessons
    :rtype: str
    """
    split_teacher = params['keyword']['word'][6:].split(' ')
    teacher = split_teacher[0].title()
    like_string = split_teacher[0][:-1].title()
    initials = split_teacher[1] if len(split_teacher) >= 2 else ''
    initials += split_teacher[2] if len(split_teacher) >= 3 else ''
    initials = initials.replace('.', '')
    if initials:
        teacher += ' '
        like_string += '%'
        for l in initials:
            like_string += l.upper() + '%'
            teacher += l.upper() + '.'

    schedule = DB.Schedule\
        .select(
            DB.Schedule.name,
            DB.Schedule.teacher,
            DB.Schedule.week,
            DB.Schedule.day,
            DB.Schedule.numb,
            DB.Schedule.room,
            DB.fn.COUNT(DB.Schedule.room).alias('groups_amount'))\
        .where(DB.Schedule.teacher.contains(like_string))\
        .order_by(
            +DB.Schedule.day,
            +DB.Schedule.numb)\
        .group_by(
            DB.Schedule.week,
            DB.Schedule.day,
            DB.Schedule.numb,
            DB.Schedule.room,
            DB.Schedule.name,
            DB.Schedule.teacher)\
        .dicts()

    delta_days = 0
    answer_content = ''
    teachers = {}
    schedule = list(schedule)
    lessons_found = False
    while not answer_content and delta_days < 30:
        date = params['date'] + dt.timedelta(days=delta_days)
        delta_days += 1
        for event in schedule:
            if date.weekday() != event['day'] \
                    or not isWeeksEqual(event['week'],
                                        date.isocalendar()[1]):
                continue

            if not answer_content:
                dname = CONST.DAY_NAMES_VINIT[date.weekday()]
                answer_content = u'Ближайшие пары в {} {}:\n\n' \
                    .format(dname, date.strftime('%d.%m'))

            name = event['name'][:20]
            name += '..' if len(event['name']) > 20 else ''
            answer_content += CONST.USER_MESSAGE[
                CONST.CMD_SEARCH_TEACHER] \
                .format(
                event['numb'],
                event['room'],
                event['groups_amount'],
                name)

            teacher = event['teacher'].replace('\n', ' + ')
            try:
                teachers[teacher] += 1
            except:
                teachers[teacher] = 1
            lessons_found = True

    if not lessons_found:
        raise Exception(CONST.ERR_NO_TEACHER_FOUND)

    if len(teachers) > 10:
        raise Exception(CONST.ERR_UNDEFINED)

    # TODO move text to CONSTS module
    if len(teachers) > 1 and not initials:
        answer = u'Напишите инициалы,'\
                 + u' т.к. найдено несколько преподавателей:\n'
        answer += ', '.join(teachers)
    else:
        answer = answer_content
        answer += u'Преподаватель ' + max(teachers)

    return answer


def cmdMyTeachers(params):
    """ Shows teachers list.
    
    :param params: same parameters for getFullSchedule function
    :type params: dict
    :return: formatted for user list of teachers
    :rtype: str
    """
    schedule_full = getFullSchedule(params)
    teachers_lessons = {}
    noteacher_counter = 0
    for event in schedule_full:
        if not event['teacher'] or len(event['teacher']) < 4:
            noteacher_counter += 1
            continue

        if teachers_lessons.get(event['teacher'], False):
            dublicate = False
            for name in teachers_lessons[event['teacher']]:
                if name == event['name']:
                    dublicate = True
                    break
            if dublicate:
                continue
            teachers_lessons[event['teacher']].append(event['name'])
        else:
            teachers_lessons[event['teacher']] = [event['name']]

    if not teachers_lessons:
        raise Exception(CONST.ERR_NO_TEACHER)

    answer = ''
    for teacher, lessons in teachers_lessons.items():
        lstr = '\n'.join(lessons)
        answer += CONST.USER_MESSAGE[CONST.CMD_MY_TEACHERS].format(
            teacher, lstr)

    answer += CONST.USER_POSTMESSAGES[CONST.CMD_MY_TEACHERS] \
        .format(noteacher_counter)

    return answer

# associate commands codes with their functions
cmd_functions = {
    CONST.CMD_LESSONS: cmdLessons,
    CONST.CMD_NEXT: cmdLessons,
    CONST.CMD_TODAY: cmdLessons,
    CONST.CMD_AFTERTOMMOROW: cmdLessons,
    CONST.CMD_TOMMOROW: cmdLessons,
    CONST.CMD_YESTERDAY: cmdLessons,
    CONST.CMD_DAY_OF_WEEK: cmdLessons,
    CONST.CMD_WEEK: cmdWeek,
    CONST.CMD_NOW: cmdLessons,
    CONST.CMD_BY_DATE: cmdLessons,
    CONST.CMD_BY_TIME: cmdLessons,
    CONST.CMD_BY_NUMB: cmdLessons,
    CONST.CMD_HELP: cmdHelp,
    CONST.CMD_POLITE: cmdPolite,
    CONST.CMD_LESSONS_TIME: cmdLessonsTime,
    CONST.CMD_TEACHER: cmdTeacher,
    CONST.CMD_LESSONS_COUNTER: cmdLessonsCounter,
    CONST.CMD_WHEN_EXAMS: cmdWhenExams,
    CONST.CMD_MAP: cmdMap,
    CONST.CMD_MYGROUP: cmdMyGroup,
    CONST.CMD_WHERE_LESSON: cmdWhereLesson,
    CONST.CMD_FOR7DAYS: cmdFor7Days,
    CONST.CMD_JUST_LESSONS: cmdLessons,
    CONST.CMD_NEW_ID: cmdNewId,
    CONST.CMD_MYID: cmdMyid,
    CONST.CMD_LINK: cmdLink,
    CONST.CMD_SEARCH_TEACHER: cmdSearchTeacher,
    CONST.CMD_MY_TEACHERS: cmdMyTeachers,
}


def findKeywords(words, text):
    """ Scan income message for command keywords.
    
    :param words: command keywords (could be regular expression)
    :type words: list
    :param text: income message text
    :type text: str
    :return: matched keyword ('idx' - list index, 'word' - word)
    :rtype: dict
    """
    keyword = {}
    for idx, word in enumerate(words):
        try:
            result = re.search(word, text).group()
        except:
            continue
        if result:
            keyword = {'idx': idx, 'word': result}
            break
    return keyword


def getGroup(params):
    """ Defines users group. 
    If there is group code in message saves it.
    If could't find user in database, creates new one with group
    code from income message.
    
    :param params: user parameters
    :type params: dict
    :return: users group ('id' - database ID, 'code' - human code)
    :return: message, if group was updated
    :rtype: dict, str
    """
    answer = ''
    vk_id = params['chat_id'] if params['chat_id'] else params[
        'user_id']
    try:
        db_user = DB.Users.get(
            DB.Users.vk_id == vk_id,
            DB.Users.is_chat == bool(params['chat_id'])
        )
        db_user.bot_activity = dt.datetime.now()
        db_user.save()
    except:
        db_user = None

    match = re.search(u'[а-я]{4}[а-я]?-[0-9]{2}-[0-9]{2}',
                      params['text'])
    msg_group = match.group(0) if match else ''
    params['text'] = params['text'].replace(msg_group, '')

    if msg_group and db_user:
        try:
            db_group = DB.Groups.get(DB.Groups.gcode == msg_group)
        except:
            raise Exception(CONST.ERR_GROUP_NOT_FOUND)
        db_user.group = db_group.id
        db_user.save()

        group_id = db_user.group.id
        group_code = db_user.group.gcode

        answer += CONST.USER_PREMESSAGE[CONST.CMD_SAVE_GROUP].format(
            msg_group.upper())
    elif msg_group:
        try:
            db_group = DB.Groups.get(DB.Groups.gcode == msg_group)
        except:
            raise Exception(CONST.ERR_GROUP_NOT_FOUND)
        db_user = DB.Users(
            vk_id=vk_id,
            is_chat=bool(params['chat_id']),
            bot_id=genBotID(vk_id),
            group=db_group.id,
            notice_today=False,
            notice_tommorow=False,
            notice_week=False,
            notice_map=False,
            send_time=None,
            notice_zerohour=None,
            bot_activity=dt.datetime.now(),
        )
        db_user.save()

        group_id = db_user.group.id
        group_code = db_user.group.gcode

        answer += CONST.USER_PREMESSAGE[CONST.CMD_SAVE_GROUP].format(
            msg_group.upper())
        answer += CONST.USER_PREMESSAGE[CONST.CMD_HELP]
    elif db_user:
        group_id = db_user.group.id
        group_code = db_user.group.gcode
    else:
        raise Exception(CONST.ERR_NO_GROUP)

    group = {
        'id': group_id,
        'code': group_code
    }
    return group, answer


# Apply hot functions
# 1 - today
# 2 - tomorrow
# 3 - week
# 4 - current on map
def applyHotFunc(command, markers):
    """ Apply hot function's codes to command and markers lists.
    
    :param command: message command
    :type command: dict
    :param markers: message markers
    :type markers: dict
    :return: defined command and marker
    :rtype: dict
    """
    func_numb = command['keyword']['word']
    if func_numb == '1':
        command['code'] = CONST.CMD_LESSONS
    if func_numb == '2':
        command['code'] = CONST.CMD_LESSONS
        markers[CONST.CMD_TOMMOROW] = {'word': '', 'idx': ''}
    if func_numb == '3':
        command['code'] = CONST.CMD_FOR7DAYS
        command['keyword']['word'] = ''
    if func_numb == '4':
        command['code'] = CONST.CMD_WHERE_LESSON

    return command, markers


def addZeroHourMsg(params):
    """ Check if it's night time and notice user about it.
    
    :param params: user parameters
    :type params: dict
    :return: formatted for user notice
    :rtype: str
    """
    app_msg = ''
    db_user = DB.Users.get(
        DB.Users.vk_id == params['vk_id'],
        DB.Users.is_chat == params['is_chat']
    )
    current_wd = dt.datetime.now().weekday()
    try:
        if db_user.notice_zerohour.weekday() != current_wd:
            app_msg = CONST.MSG_ZERO_HOUR.format(
                CONST.DAY_NAMES[current_wd])
    except:
        pass
    db_user.notice_zerohour = dt.datetime.now()
    db_user.save()

    return app_msg


# noinspection PyTypeChecker
def analize(params):
    """ CORE. Implements algorithm that generates answer 
    based on income user message.
    1. Get user's group.
    2. Set default settings.
    3. Define message's command. (what user waiting for)
    4. Define command's datetime markers.
    5. Apply defined markers on command settings.
    6. Perform command and generate answer message for user. 
    
    :param params: user and message data
    :type params: dict
    :return: answer ('text' - message text, 'attachment' - ...)
    :rtype: dict
    """
    global attachment
    attachment = ''

    # 1. Get user's group.
    group, msg_head = getGroup(params)

    # 2. Set default settings.
    answer_ok = bool(msg_head)
    markers = {}
    default_kwd = {'word': u'сегодня', 'idx': 0}
    command = {
        'code': CONST.CMD_LESSONS,
        'keyword': default_kwd
    }
    date = dt.datetime.today()
    lesson = 0
    find_first = False

    # 3. Define message's command. (what user waiting for)
    for cmd, keywords in CONST.KEYWORDS.items():
        if cmd in CONST.MARKERS:
            continue
        word = findKeywords(keywords, params['text'])
        if word and (command['code'] >= cmd):
            command['code'] = cmd
            command['keyword'] = word
            answer_ok = True
    if answer_ok:
        params['text'] = params['text'].replace(
            command['keyword']['word'], '')

    # 4. Define command's datetime markers.
    for cmd, keywords in CONST.KEYWORDS.items():
        if not cmd in CONST.MARKERS:
            continue
        word = findKeywords(keywords, params['text'])
        if word:
            params['text'] = params['text'].replace(word['word'], '')
            markers[cmd] = word

    if command['code'] == CONST.CMD_HOT_FUNC:
        command, markers = applyHotFunc(command, markers)

    if answer_ok and not markers:
        markers = {CONST.CMD_TODAY: default_kwd}

    # 5. Apply defined markers on command settings.
    for cmd_code, keyword in markers.items():
        if cmd_code == CONST.CMD_TOMMOROW:
            date = dt.datetime.today() + dt.timedelta(days=1)
        elif cmd_code == CONST.CMD_NOW:
            lesson = int(getLessonNumb(dt.datetime.now().time()))
        elif cmd_code == CONST.CMD_NEXT:
            lesson = int(getLessonNumb(dt.datetime.now().time())) + 1
        elif cmd_code == CONST.CMD_AFTERTOMMOROW:
            date = dt.datetime.today() + dt.timedelta(days=2)
        elif cmd_code == CONST.CMD_YESTERDAY:
            date = dt.datetime.today() - dt.timedelta(days=1)
        elif cmd_code == CONST.CMD_DAY_OF_WEEK:
            keyword['word'] = CONST.DAY_NAMES_VINIT[keyword['idx']]
            for i in range(0, 7):
                temp_date = dt.datetime.today() + dt.timedelta(days=i)
                if temp_date.weekday() == keyword['idx']:
                    date = temp_date
                    break
        elif cmd_code == CONST.CMD_BY_NUMB:
            lesson = keyword['idx']
            keyword['word'] = keyword['idx']
        elif cmd_code == CONST.CMD_BY_TIME:
            try:
                lesson = getLessonNumb(
                    dt.datetime.strptime(keyword['word'],
                                         '%H:%M').time())
            except:
                del markers[cmd_code]
        elif cmd_code == CONST.CMD_BY_DATE:
            try:
                year = str(dt.date.today().year)
                date = dt.datetime.strptime(keyword['word'] + year,
                                            '%d.%m%Y')
            except:
                try:
                    day, month = keyword['word'].split(' ')
                    mnumb = 0
                    for idx, name in enumerate(CONST.MONTH_NAMES):
                        if re.search(name, month):
                            mnumb = idx + 1
                            break
                    date = dt.date(2017, mnumb, int(day))
                except:
                    del markers[cmd_code]
        elif cmd_code == CONST.CMD_FIRST:
            find_first = True

    # Prepare parametrs for functions 
    cmd_params = {
        'vk_id': params['chat_id'] if params['chat_id'] else params[
            'user_id'],
        'is_chat': bool(params['chat_id']),
        'group': group,
        'date': date,
        'day': date.weekday(),
        'week': date.isocalendar()[1],
        'lnumb': lesson,
        'keyword': command['keyword'],
        'find_first': find_first
    }

    # 6. Perform command and generate answer message for user.
    # Check markers after apply
    markers_text = ''
    for cmd, kwd in markers.items():
        markers_text += CONST.USER_PREMESSAGE[cmd].format(kwd['word'])
        answer_ok = True
    if not answer_ok:
        LOGGER.log(CONST.LOG_MESGS, params['text'])
        raise Exception(CONST.ERR_SKIP)

    # Perform command and check for result
    msg_head += CONST.USER_PREMESSAGE[command['code']].format(
        markers=markers_text)
    cmd_outcome = cmd_functions[command['code']](cmd_params)
    msg_body = cmd_outcome['text']
    attachment = cmd_outcome['attachment']

    msg_footer = ''
    if dt.datetime.now().hour < 2:
        msg_footer = addZeroHourMsg(cmd_params)

    answer = {
        'text': msg_head + msg_body + msg_footer,
        'attachment': attachment
    }
    return answer


def genAnswer(params):
    """ Genrates answer for income message. 
    Adds new message parameters and save message if it's
    for developer.
    
    :param params: user and message parameters
    :type params: dict
    :return: answer ('text' - answer text,'attachment' - some media)
    :rtype: dict
    """
    global attachment
    attachment = ''
    answer = {
        'text': '',
        'attachment': ''
    }

    params['text'] = params['text'].lower()

    # Check for chat
    if params['chat_id'] and not any(
            re.match('^' + word, params['text']) for word in
            CONST.CHAT_KEYWORDS):
        raise Exception(CONST.ERR_SKIP)

    # Check feedback
    if any(re.search(word, params['text']) for word in
           CONST.FEEDBACK_KEYWORDS):
        LOGGER.log(CONST.LOG_FBACK,
                   str(params['user_id']) + ' ' + params['text'])
        answer['text'] = CONST.USER_PREMESSAGE[CONST.CMD_FEEDBACK]
    else:
        answer = analize(params)

    return answer


def isNoticeTime():
    """ Check current time to be in notice time range.
    
    :return: true if in range, false if not
    :rtype: bool
    """
    today = dt.datetime.now()
    return (
        CONST.NOTICE_START_HOUR <= today.hour <= CONST.NOTICE_END_HOUR)


def saveNoticeTime(notice):
    """ Saves in database time of last user notice.
    
    :param notice: notice parameters
    :type notice: dict
    :return: was it successful or not
    :rtype: bool
    """
    try:
        user = DB.Users.get(DB.Users.vk_id == notice['user_id'],
                            DB.Users.is_chat == notice['is_chat'])
        user.send_time = dt.datetime.now()
        user.save()
        success = True
    except:
        success = False

    return success


def getNotice():
    """ Retrieve notice code from database and perform it.
    
    :return: notice, witch looks like bot answer for user
    :rtype: dict 
    """
    today = dt.datetime.now()
    notice = {
        'user_id': '',
        'is_chat': '',
        'text': '',
        'attachment': '',
    }

    user = None
    users = DB.Users.select().where((
        DB.Users.notice_today |
        DB.Users.notice_tommorow |
        DB.Users.notice_week |
        DB.Users.notice_map
    ), (
        (DB.Users.send_time >> None) |
        (DB.Users.send_time < dt.datetime(today.year, today.month,
                                          today.day))
    )).limit(1)

    for u in users:
        user = u
        notice['user_id'] = user.vk_id
        notice['is_chat'] = user.is_chat
        break

    if not user:
        return notice

    params = {
        'user_id': user.vk_id,
        'chat_id': user.vk_id if user.is_chat else False,
        'text': ''
    }

    def appendAnswer(notice, msg):
        try:
            params['text'] = msg
            answer = genAnswer(params)
            notice['text'] += '\n\n' + answer['text']
            notice['attachment'] += '\n' + answer['attachment']
        except:
            pass
        return notice

    if user.notice_today and today.weekday() != 6:
        notice = appendAnswer(notice, CONST.MSG_NOTICE_TODAY)
    if user.notice_tommorow and today.weekday() != 5:
        notice = appendAnswer(notice, CONST.MSG_NOTICE_TOMORROW)
    if user.notice_week and today.weekday() == 6:
        notice = appendAnswer(notice, CONST.MSG_NOTICE_WEEK)
    if user.notice_map and today.weekday() != 6:
        notice = appendAnswer(notice, CONST.MSG_NOTICE_MAP)

    if not (notice['text'] or notice['attachment']):
        saveNoticeTime(notice)
        raise Exception()

    return notice
