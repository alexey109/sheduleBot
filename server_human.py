#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time

import security
import core
import consts as CONST


class UsersStack:
    """ 
    Prologue: VK API have some limits. If you want use API without 
    problems, you should control API calls frequency.

    This class implements special history of bot answer time for 
    users. Every user has limit message number in one time period,
    that number and time value described in CONSTS module.
    Example: user could write 5 message in 2 minutes.
    """

    def __init__(self):
        """ Initialize list of user's time.        
        """
        self.stack = []

    def getRest(self, user_id):
        """ Lookup for user's answers time history, and define how 
        much messages and time left.

        :param user_id: user's ID
        :return: rest messages number
        :return: rest time amount
        :rtype: int, float
        """
        now = int(time.time())
        try:
            while (now - self.stack[0][1]) >= CONST.USERS_QUEUE_LEN:
                del self.stack[0]
        except:
            pass

        user_time = [user_id, now]
        amount = 0
        max_time = 0
        for rec in self.stack:
            if rec[0] == user_time[0]:
                tdiff = now - rec[1]
                if tdiff > max_time:
                    max_time = tdiff
                amount += 1

        msg_rest = CONST.USER_MSG_AMOUNT - amount
        if msg_rest > 0:
            self.stack.append(user_time)

        return msg_rest, CONST.USERS_QUEUE_LEN - max_time


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = raw_input("Enter captcha code {0} : ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def main():
    vk_session = vk_api.VkApi(security.user_login, security.user_password, captcha_handler=captcha_handler)
    vk_session.auth()
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    usr_stack = UsersStack()
    answer_time = time.time()
    for event in longpoll.listen():
        if not (event.type == VkEventType.MESSAGE_NEW and event.to_me):
            continue

        params = {
            'msg_id': None,
            'user_id': event.user_id,
            'chat_id': event.chat_id,
            'text': event.text,
            'new_group': False
        }

        answer = {
            'text': '',
            'attachment': ''
        }
        try:
            answer = core.genAnswer(params)
        except Exception as e:
            if e.args[0] == CONST.ERR_SKIP:
                continue
            if e.args[0] in CONST.ERR_MESSAGES.keys():
                answer['text'] = CONST.ERR_MESSAGES[e.args[0]]
            else:
                answer['text'] = CONST.ERR_MESSAGES[CONST.ERR_UNDEFINED]
            print str(e)

        if not answer['text'] and not answer['attachment']:
            answer['text'] = CONST.ERR_MESSAGES[CONST.ERR_DUMMY]

        if event.chat_id:
            peer = 2000000000 + event.chat_id
        else:
            peer = event.user_id
            answer['text'] += u'\n\nУбедительная просьба писать личные сообщения через новое сообщество vk.com/mtu_timetable.'

        msg_rest, time_rest = usr_stack.getRest(peer)
        if msg_rest == 0:
            continue
        if msg_rest == 1:
            answer['text'] += CONST.ERR_MESSAGES[CONST.ERR_MSG_LIMIT].format(time_rest)


        if time.time() - answer_time < 0.3:
            time.sleep(1)
        if answer['attachment']:
            vk.messages.send(
                peer_id=peer,
                attachment=answer['attachment'],
                message=answer['text']
            )
        else:
            vk.messages.send(
                peer_id=peer,
                message=answer['text']
            )
        answer_time = time.time()


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print e
            time.sleep(30)
