#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk_api
import time

import security
import core

def main():
    vk_session = vk_api.VkApi(security.user_login, security.user_password)
    vk_session.auth()
    vk = vk_session.get_api()

    have_notice = True
    chat_notice = True
    while have_notice:
        notice = core.getNotice(for_chat=chat_notice)
        if not notice['user_id'] and chat_notice:
            chat_notice = False
            vk_session = vk_api.VkApi(token=security.group_token)
            vk = vk_session.get_api()
        elif not notice['user_id']:
            have_notice = False
            break

        time.sleep(30)
        if notice['is_chat']:
            peer = 2000000000 + int(notice['user_id'])
        else:
            peer = notice['user_id']

        if notice['attachment']:
            vk.messages.send(
                peer_id=peer,
                attachment=notice['attachment'],
                message=notice['text']
            )
        else:
            vk.messages.send(
                peer_id=peer,
                message=notice['text']
            )

    return True


if __name__ == '__main__':
    close = False
    while not close:
        try:
            close = main()
        except Exception as e:
            print e
