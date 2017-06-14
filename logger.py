#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime as dt
import codecs
import re

import consts as CONST


def fwrite(fname, text):
    """ Add text to files with adding date and time.
    
    :param fname:  file name
    :type fname: str
    :param text: some text
    :type text: str
    """
    with codecs.open(fname, 'a', 'utf-8') as f:
        f.write(u"{};{};{} \n".format(
            dt.datetime.now().strftime('%Y.%m.%d'),
            dt.datetime.now().strftime('%H:%M:%S'),
            text)
        )
        f.close()


def exception(e):
    """ Perform exception saving.
    
    :param e: exception
    :type e: object
    """
    desc = str(e)
    try:
        if isinstance(e.args[0], int):
            desc = 'Code: %s Text: %s' % (
                str(e.args[0]), CONST.ERR_MESSAGES[e.args[0]])
    except:
        pass
    fname = CONST.LOG_DIR + CONST.LOG_ERROR_FILE
    fwrite(fname, desc)


def workload(text):
    """ Saves workload statistics.
    
    :param text: staticstic information.
    :type text: str
    """
    fname = CONST.LOG_DIR + CONST.LOG_WLOAD_FILE
    fwrite(fname, text)


def feedback(text):
    """ Saves feedback messages.
    
    :param text: message text
    :type text: str
    """
    fname = CONST.LOG_DIR + CONST.LOG_FBACK_FILE
    fwrite(fname, text)


def messages(text):
    """ Saves any message.
    
    :param text: message text
    :type text: str
    """
    fname = CONST.LOG_DIR + CONST.LOG_MESGS_FILE
    fwrite(fname, text)


def statistics(args):
    """ Saves statistics.
    
    :param args: statistic information
    :type args: list
    """
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


def log(code, arg):
    """ Define what command perform using anguments.
    
    :param code: command code
    :type code: int
    :param arg: arguments
    :type arg: str, list
    """
    if not CONST.LOG:
        return None

    try:
        if code == CONST.LOG_ERROR:
            exception(arg)
        elif code == CONST.LOG_WLOAD:
            workload(arg)
        elif code == CONST.LOG_FBACK:
            feedback(arg)
        elif code == CONST.LOG_MESGS:
            messages(arg)
        elif code == CONST.LOG_STATS:
            statistics(arg)
    except:
        pass
