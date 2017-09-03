#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk
import time

import security
import core
import logger as LG
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


class ClientVK:
    """
    Operates with income messages, sends notifications and answers.
    Uses VK API methods to operate with vkontakte social net.
    """
    def __init__(self):
        self.logger = LG.Logger()
        self.last_call = 0
        self.usr_stack = UsersStack()

    def waitNextCall(last_call, delta):
        """ Make pause for 0.3 seconds if it have passed less than delta
        time from last call time.

        :param last_call: last call time
        :type last_call: float
        :param delta: delta time
        :type delta: float
        """
        while (time.time() - last_call) < delta:
            time.sleep(0.3)

    # Open vkAPI session
    # Return type: vk.api object
    def openSession(self):
        """ Open VK API session using parameters from security module.
        
        :return: vk api object
        :rtype: object
        """
        success = False
        while not success:
            try:
                session = vk.AuthSession(
                    app_id=security.app_id,
                    user_login=security.user_login,
                    user_password=security.user_password,
                    scope=security.scope)
                api = vk.API(session, v='5.60', lang='ru')
                success = True
            except Exception as e:
                self.logger.log(CONST.LOG_ERROR, e)
                time.sleep(3)
        return api

    def retriveBody(self, vk_msg):
        """ Retrieves message text from all forward messages.
        
        :param vk_msg: message object
        :type vk_msg: object
        :return: combined text from all messages
        :rtype: str
        """
        body = vk_msg.get('body', '')
        fwd_messages = vk_msg.get('fwd_messages', [])
        for msg in fwd_messages:
            body += ' ' + self.retriveBody(msg) + ' '

        return body

    def sendMyAnswer(self, vk_msg):
        """ Gets answer for message from core and sents it back 
        for user. Could sent to single and group dialogs.
        
        :param vk_msg: message object
        :type vk_msg: object
        """
        answer = {
            'text': '',
            'attachment': ''
        }

        msg_text = self.retriveBody(vk_msg)
        params = {
            'msg_id': vk_msg['id'],
            'user_id': vk_msg.get('user_id', 0),
            'chat_id': vk_msg.get('chat_id', 0),
            'text': msg_text,
            'new_group': False
        }

        if not params['chat_id']:
            self.waitNextCall(self.last_call, 0.5)
            self.api.messages.markAsRead(message_ids=params['msg_id'],
                                         peer_id=params['user_id'])

        try:
            answer = core.genAnswer(params)
        except Exception as e:
            if isinstance(e.args[0], int):
                answer['text'] = CONST.ERR_MESSAGES[e.args[0]]
            else:
                self.logger.log(CONST.LOG_ERROR, e)
                answer['text'] = CONST.ERR_MESSAGES[
                    CONST.ERR_UNDEFINED]

        if answer['text'] or answer['attachment']:
            msg_rest, time_rest = self.usr_stack.getRest(
                params['user_id'])
            if (msg_rest == 0):
                return
            if msg_rest == 1:
                answer['text'] += CONST.ERR_MESSAGES[
                    CONST.ERR_MSG_LIMIT].format(time_rest)
            self.logger.log(CONST.LOG_STATS,
                            [params['user_id'], msg_text,
                             answer['text'][:100]])

            self.waitNextCall(self.last_call, 1)
            if params['chat_id']:
                self.api.messages.send(
                    chat_id=params['chat_id'],
                    message=answer['text'],
                    attachment=answer['attachment']
                )
            else:
                self.api.messages.send(
                    user_id=params['user_id'],
                    message=answer['text'],
                    attachment=answer['attachment']
                )

            self.last_call = time.time()

    def sendNotice(self):
        """ Get notice from core and sent it to user.
        
        :return: have send or not
        :rtype: bool
        """
        notice = core.getNotice()
        if not notice['user_id']:
            return False

        self.waitNextCall(self.last_call, CONST.NOTICE_DELAY)
        if notice['is_chat']:
            self.api.messages.send(
                chat_id=notice['user_id'],
                message=notice['text'],
                attachment=notice['attachment']
            )
        else:
            self.api.messages.send(
                user_id=notice['user_id'],
                message=notice['text'],
                attachment=notice['attachment']
            )
        core.saveNoticeTime(notice)

        self.last_call = time.time()
        return True

    # Scan enter messages and answer
    def run(self):
        """ Checks for new messages, handles it and send notice
         if it's notification time.
            
        :return: 
        :rtype: 
        """
        self.api = self.openSession()
        last_get_call = time.time() - 10
        while 1:
            try:
                self.waitNextCall(self.last_call, 1)
                toffset = int(time.time() - last_get_call)
                toffset = toffset if toffset > 10 else 10
                response = self.api.messages.get(out=0, count=10,
                                                 time_offset=toffset,
                                                 preview_length=100)
                self.last_call = time.time()
                last_get_call = time.time()
                unread_msgs = []
                for vk_msg in response['items']:
                    if vk_msg['read_state'] == 0:
                        unread_msgs.append(vk_msg)
                if unread_msgs:
                    for vk_msg in unread_msgs:
                        try:
                            self.sendMyAnswer(vk_msg)
                        except Exception as e:
                            self.logger.log(CONST.LOG_ERROR, e)
                            self.api = self.openSession()
                elif core.isNoticeTime():
                    try:
                        self.sendNotice()
                    except Exception as e:
                        self.logger.log(CONST.LOG_ERROR, e)
                        self.api = self.openSession()

            except Exception as e:
                print str(e)
                print 'Try to open new session'
                self.logger.log(CONST.LOG_ERROR, e)
                self.api = self.openSession()
                print 'Session was opened'


vk_client = ClientVK()
vk_client.run()
