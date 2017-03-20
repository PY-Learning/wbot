# -*- encoding: utf-8 -*-
import logging

import itchat
from wbot.core.base import BaseModule
from wbot.core.types import MessageType


class RecallModule(BaseModule):
    def handle(self, msg, msg_type, sender_type, background=False):
        #  TODO: RecallModule handle
        key = '{}:{}'.format(msg['FromUserName'], msg['RefMsgId'])
        group_name = itchat.search_chatrooms(userName=msg['FromUserName']).get('NickName')
        try:
            replay_text = '{} recall message is {}'.format(msg['ActualNickName'], itchat.get_cache(key))
            logging.info('group {}: {}: recall message is {}'.format(
                group_name, msg['ActualNickName'], replay_text))
        except KeyError as e:
            logging.error('Keyerror {}'.format(str(e)))
            return

        return replay_text, msg['FromUserName']
        pass

    def match(self, msg, msg_type, sender_type) -> int:
        if msg_type == MessageType.Recall:
            return self.CERTAINLY
        else:
            return self.BACKGROUND
