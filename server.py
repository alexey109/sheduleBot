#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time

import security
import core
import consts as CONST

def main():
    vk_session = vk_api.VkApi(token=security.group_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    answer_time = time.time()
    for event in longpoll.listen():
        if not (event.type == VkEventType.MESSAGE_NEW and event.to_me):
            continue

        params = {
            'msg_id': None,
            'user_id': event.user_id,
            'chat_id': None,
            'text': event.text,
            'new_group': True
        }

        answer = {
            'text': '',
            'attachment': ''
        }
        try:
            answer = core.genAnswer(params)
        except Exception as e:
            if e.args[0] in CONST.ERR_MESSAGES.keys():
                answer['text'] = CONST.ERR_MESSAGES[e.args[0]]
            else:
                answer['text'] = CONST.ERR_MESSAGES[CONST.ERR_UNDEFINED]
            print str(e)

        if not answer['text'] and not answer['attachment']:
            answer['text'] = CONST.ERR_MESSAGES[CONST.ERR_DUMMY]

        if time.time() - answer_time < 0.3:
            time.sleep(0.4)
        if answer['attachment']:
            vk.messages.send(
                user_id=event.user_id,
                attachment=answer['attachment'],
                message=answer['text']
            )
        else:
            vk.messages.send(
                user_id=event.user_id,
                message=answer['text']
            )
        answer_time = time.time()


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print e
            time.sleep(5)
