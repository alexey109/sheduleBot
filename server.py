#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import time

import security
import core
import consts as CONST


def main():
    vk_session = vk_api.VkApi(token=security.group_token)
    longpoll = VkBotLongPoll(vk_session, security.group_id)

    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('сегодня', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('завтра', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('пары на неделю', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('первые на неделю', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('где сейчас пара', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('где будет пара', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('кто сейчас лектор', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('список учителей', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('время звонков', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('сколько осталось', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('счётчик', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('сколько осталось', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('глупый бот', color=VkKeyboardColor.PRIMARY)

    vk = vk_session.get_api()
    answer_time = time.time()
    for event in longpoll.listen():
        if not (event.type == VkBotEventType.MESSAGE_NEW):
            continue

        params = {
            'msg_id': None,
            'user_id': event.obj.peer_id,
            'chat_id': None,
            'text': event.obj.text,
            'new_group': True
        }

        answer = {
            'text': '',
            'attachment': ''
        }
        try:
            answer = core.genAnswer(params)
        except CONST.GroupException as ge:
            answer['text'] = CONST.ERR_MESSAGES[ge.args[0]]
            answer['text'] += ge.suggestion
        except Exception as e:
            if e.args[0] in CONST.ERR_MESSAGES.keys():
                answer['text'] = CONST.ERR_MESSAGES[e.args[0]]
            else:
                answer['text'] = CONST.ERR_MESSAGES[CONST.ERR_UNDEFINED]
                print str(e)
                continue

        if not answer['text'] and not answer['attachment']:
            answer['text'] = CONST.ERR_MESSAGES[CONST.ERR_DUMMY]

        if time.time() - answer_time < 0.1:
            time.sleep(0.1)

        msg_buttons = None
        if event.from_user:
            msg_buttons = keyboard.get_keyboard()
        if answer['attachment']:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                attachment=answer['attachment'],
                message=answer['text'],
                keyboard=msg_buttons
            )
        else:
            vk.messages.send(
                peer_id=event.obj.peer_id,
                message=answer['text'],
                keyboard=msg_buttons
            )
        answer_time = time.time()


if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print e
            time.sleep(5)
