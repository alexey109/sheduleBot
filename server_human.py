#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import time

import security
import core
import consts as CONST

def main():
    vk_session = vk_api.VkApi(security.user_login, security.user_password)
    vk_session.auth()
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    answer_time = time.time()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            params = {
                'msg_id': None,
                'user_id': event.user_id,
                'chat_id': event.chat_id,
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

            if time.time() - answer_time < 0.3:
                time.sleep(time.time() - answer_time)
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
    main()