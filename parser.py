#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from openpyxl import load_workbook
import re


def safeGet(lst, idx, default):
    """ Helpful function if you want to get list value by idx.
    
    :param lst: list
    :type lst: list
    :param idx: value index
    :type idx: int
    :param default: return it if index out of list 
    :type default: any
    :return: 'default' argument 
    :rtype: any
    """
    try:
        return lst[idx]
    except:
        return default


class Parser:
    """
    Retrieves schedule from excel document.
    """

    def openDoc(self, doc_name):
        """ Open excel-document.
        
        :param doc_name: document location with name
        :type doc_name: str
        :return: document object
        :rtype: object
        """
        result = True
        try:
            self.wb = load_workbook(filename=doc_name)
        except Exception as e:
            result = False
        return result

    def splitBody(self, text):
        """ In documents main lesson information contains in one cell.
        Thus function parse text from that cell.
        
        :param text: text from cell
        :type text: str
        :return: lessons information
        :rtype: list
        """
        text = text.replace(u'\n', ' ')
        text = text.replace(u'н.', '') + '.'  # Bag fix :(

        ST_BODY = 0
        ST_PARAMS = 1
        ST_WEEK = 2

        teacher_kwd = [u'асс', u'доц', u'проф', u'ст.', u'ст ',
                       u'преп']

        rules = {
            ST_BODY: [
                {'expr': u'[А-Яа-я\./\s]', 'link': ST_BODY,
                 'ext': False, 'new_param': False},
                {'expr': '[0-9I]', 'link': ST_WEEK, 'ext': True,
                 'new_param': False},
                {'expr': '\(', 'link': ST_PARAMS, 'ext': False,
                 'new_param': True},
            ],
            ST_PARAMS: [
                {'expr': '[^\)]', 'link': ST_PARAMS, 'ext': False,
                 'new_param': False},
                {'expr': '\)', 'link': ST_BODY, 'ext': False,
                 'new_param': False},
            ],
            ST_WEEK: [
                {'expr': '[0-9I,\-\s]', 'link': ST_WEEK, 'ext': False,
                 'new_param': False},
                {'expr': '[^0-9I,\-\s]', 'link': ST_BODY,
                 'ext': False, 'new_param': False},
            ]
        }

        status = ST_BODY
        i = 0
        body = {}
        params = []
        name = week = teacher = ''
        for idx, l in enumerate(text):
            for rule in rules[status]:
                if re.search(rule['expr'], l):
                    status = rule['link']
                    if (rule['ext'] and name) or (
                                idx == len(text) - 1):
                        for word in teacher_kwd:
                            pos = name.find(word)
                            if pos > 0:
                                teacher = name[pos:]
                                name = name[:pos]
                                break

                        body[i] = {}
                        body[i]['name'] = name.strip()
                        body[i]['teacher'] = teacher.strip()
                        body[i]['params'] = params
                        body[i]['week'] = week.strip()
                        name = week = teacher = ''
                        params = []
                        i += 1
                    if rule['new_param']:
                        params.append('')
                    break

            if l in ['(', ')']:
                continue

            if status == ST_BODY:
                name += l
            elif status == ST_PARAMS:
                params[-1] += l
            elif status == ST_WEEK:
                week += l

        return body

    def getGroupSchdl(self, schedule, sheet):
        """ Look up for one column and get schedule for one group.
        
        :param schedule: full schedule
        :type schedule: dict
        :param sheet: excel sheet object
        :type sheet: object
        :return: schedule with new added group
        :rtype: dict
        """

        def isEventEqual(event1, event2):
            """ Check two lesson for equation.
            
            :return: Equal or not
            :rtype: bool
            """
            equal = False
            if event1['day'] == event2['day'] \
                    and event1['numb'] == event2['numb'] \
                    and event1['room'] == event2['room'] \
                    and event1['name'] == event2['name'] \
                    and event1['teacher'] == event2['teacher']:
                try:
                    params = True
                    for i in range(0, len(event1['params'])):
                        if params and (
                                    event1['params'][i] !=
                                    event2['params'][i]):
                            params = False
                except:
                    params = False

                if params and 'I' in event1['week'] \
                        and 'I' in event2['week']:
                    equal = True
            return equal

        def checkFullDay(name):
            """ Check if full day event on a day.
            
            :param name: cell value
            :type name: str
            :return: is full day event or not
            :rtype: bool
            """
            keywords = [u'воен', u'производств.*практ',
                        u'день.*самост']
            find = False
            for keyword in keywords:
                if re.search(keyword, name.lower()):
                    find = True
                    break
            return find

        for row in sheet.iter_rows(min_row=2,
                                   max_col=sheet.max_column,
                                   max_row=2):
            for cell in row:
                lector_flag = False
                if not cell.internal_value:
                    continue
                try:
                    match = re.search(
                        u"[А-Яа-я]{4}[А-Яа-я]?-[0-9]{2}-[0-9]{2}",
                        cell.internal_value)
                    if not match:
                        continue
                except:
                    continue
                j = cell.col_idx
                group = cell.internal_value.lower()
                lections = []
                maybe_room = sheet.cell(row=3,
                                        column=j + 3).internal_value
                if maybe_room and (u'ауд' in maybe_room):
                    lector_flag = True

                for i in range(4, 76):
                    content = sheet.cell(row=i,
                                         column=j).internal_value
                    if not content:
                        continue
                    etype = sheet.cell(row=i,
                                       column=j + 1).internal_value
                    etype = etype.split('\n') if etype else ''
                    if lector_flag:
                        lector = sheet.cell(row=i,
                                            column=j + 2) \
                            .internal_value
                        rooms = sheet.cell(row=i,
                                           column=j + 3) \
                            .internal_value
                    else:
                        lector = ''
                        rooms = sheet.cell(row=i,
                                           column=j + 2) \
                            .internal_value
                    rooms = rooms.split('\n') if rooms else []

                    cell_day = (i - 4) / 12
                    cell_numb = (i - cell_day * 12) / 2 - 1
                    cell_week = 'I' if (i - cell_day * 12) % 2 == 0 \
                        else 'II'
                    info = self.splitBody(content)
                    for i in range(0, len(info)):
                        event_type = safeGet(etype, i, '')
                        room = safeGet(rooms, i, '-')

                        if len(info[i]['name']) < 2:
                            continue
                        event = {
                            'day': cell_day,
                            'numb': cell_numb,
                            'room': room,
                            'week': info[i]['week'] if info[i][
                                'week'] else cell_week,
                            'name': info[i][
                                        'name'] + ' ' + event_type,
                            'teacher': lector,
                            'params': info[i]['params']
                        }

                        append_flag = True
                        for l in lections:
                            if isEventEqual(l, event):
                                l['week'] = ''
                                append_flag = False

                        if append_flag:
                            if checkFullDay(event['name']):
                                event['week'] = ''
                                event['numb'] = 1
                            lections.append(event)

                schedule[group] = lections

        return schedule

    def getSchedule(self, document):
        """ Retrieves groups schedule from excel document.
        
        :param document: document location with name
        :type document: str
        :return: schedule type (lections/exams/zachet)
        :return: groups schedule
        :rtype: dict
        """
        if not self.openDoc(document):
            return {}

        schedule = {}
        schdl_type = 'lections'
        for sheet in self.wb:
            schdl_type = 'lections'
            exam = False

            for row in sheet.iter_rows(min_row=1,
                                       max_col=sheet.max_column,
                                       max_row=3):
                for cell in row:
                    try:
                        group_name = cell.internal_value
                        if u'экзамен' in group_name.lower():
                            exam = True
                            schdl_type = 'exams'
                    except:
                        pass

            if not exam:
                schedule = self.getGroupSchdl(schedule, sheet)

        return schdl_type, schedule
