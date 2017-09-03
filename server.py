#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import security
import core
import consts as CONST

def main():
    vk_session = vk_api.VkApi(token=security.group_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
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


if __name__ == '__main__':
    main()