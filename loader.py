#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2
import re
from os import listdir, makedirs
from os.path import isfile, join
from optparse import OptionParser
import shutil
import datetime as dt

import consts as CONST
import parser as pr
import dbmodels as db


def adjustText(text, max_len=20, end_len=-4):
    if len(text) < max_len:
        return text
    start = text[:(max_len + end_len - 2)] + '..'
    end = text[end_len:]

    return start + end

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


if user_options.download:
    print "Try to get html code from mirea schedule page."
    try:
        response = urllib2.urlopen('https://www.mirea.ru/education/schedule-main/schedule/')
        html = response.read()
        print 'HTML got succesfull.'
        response.close()
    except Exception as e:
        print 'HTML got with errors!'

    print 'Try to load excel documents.'
    counter = 0
    doc_urls = re.findall('[^"]*\.xlsx?', html)
    print 'Document amount = ' + str(len(doc_urls))
    try:
        shutil.rmtree(CONST.SCHEDULE_DIR)
    except:
        pass
    makedirs(CONST.SCHEDULE_DIR)
    for i, url in enumerate(doc_urls):
        try:
            ftype = re.search('\.[a-z]*\Z', url).group()
            try:
                doc = urllib2.urlopen(url).read()
            except Exception as e:
                print '--- Exception\n' + url + '\n' + str(e) + '\n---\n'
            with open(CONST.SCHEDULE_DIR + str(i) + ftype,'wb') as f:
                f.write(doc)
                f.close()
            counter += 1
        except Exception as e:
            print '--- Exception\n' + url + '\n' + str(e) + '\n---\n'
    print 'Document loaded succesfull. Count = ' + str(counter)

documents = [f for f in listdir(CONST.SCHEDULE_DIR) if
             isfile(join(CONST.SCHEDULE_DIR, f))]

print 'Load schedule to database'
parser = pr.Parser()
print u'Документов:' + str(len(documents))
count = 0
for doc in documents:
    count += 1
    print u'Загрузка документа №' + str(count) + '\r'
    try:
        schdl_type, schedule = parser.getSchedule(
            CONST.SCHEDULE_DIR + doc)
    except Exception as e:
        print e
        continue

    if schdl_type == user_options.type == 'lections':
        for group, events in schedule.items():
            try:
                group_obj, flag = db.Groups.get_or_create(gcode=group[:20])
                old_gschedule = list(db.Schedule.select().where(db.Schedule.group == group_obj.id))
                query = db.Schedule.delete().where(db.Schedule.group == group_obj.id)
                query.execute()
            except Exception as e:
                print e
                continue

            not_found_events = []
            for event in events:
                try:
                    nname = event['name']
                    for par in event['params']:
                        nname += " (" + par + ")"
                    nteacher = event['teacher'] if event[
                        'teacher'] else ''
                    nroom = unicode(event['room'])[:20] if event['room'] else ''
                    schdl_obj = db.Schedule(
                        group=group_obj,
                        week=event['week'],
                        day=event['day'],
                        numb=event['numb'],
                        name=nname,
                        room=nroom,
                        teacher=nteacher,
                    )
                    find = False
                    i = 0
                    while i < len(old_gschedule):
                        old_event = old_gschedule[i]
                        if old_event.day == schdl_obj.day \
                            and old_event.numb == schdl_obj.numb \
                            and old_event.week == schdl_obj.week \
                            and old_event.name == schdl_obj.name \
                            and old_event.room == schdl_obj.room \
                            and old_event.teacher == schdl_obj.teacher:
                            find = True
                            old_gschedule.pop(i)
                            continue
                        i += 1

                    if not find:
                        not_found_events.append(schdl_obj)

                    schdl_obj.save()
                except Exception as e:
                    print e
                    continue

            if not (old_gschedule or not_found_events):
                continue

            old_fields = ';'.join(
                [u'- "{}., {} пара, {} н., {}, ауд. {}"'.format(
                    CONST.DAY_NAMES_SHORT[i.day],
                    i.numb,
                    adjustText(i.week, 8, -3),
                    adjustText(i.name),
                    i.room if i.room else '-'
                ) for i in old_gschedule])
            new_fields = ';'.join(
                [u'+ "{}., {} пара, {} н., {}, ауд. {}"'.format(
                    CONST.DAY_NAMES_SHORT[i.day],
                    i.numb,
                    adjustText(i.week, 8, -3),
                    adjustText(i.name),
                    i.room if i.room else '-'
                ) for i in not_found_events])
            his_rec = db.History(
                group=group_obj,
                old_fields=old_fields[:999],
                new_fields=new_fields[:999],
                date=dt.datetime.today().date()
            )
            his_rec.save()
