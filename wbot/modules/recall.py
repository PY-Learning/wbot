# -*- encoding: utf-8 -*-
import itchat
from wbot.core.base import BaseModule
from wbot.core.types import MessageType
from wbot.ext.log import error, info


class RecallModule(BaseModule):
    CONFIG_PREFIX = "RECALL"

    @classmethod
    def init_from(cls, bot):
        return cls()

    def handle(self, msg, msg_type, sender_type, background=False):
        #  TODO: RecallModule handle
        key = '{}:{}'.format(msg['FromUserName'], msg['RefMsgId'])
        group_name = itchat.search_chatrooms(userName=msg['FromUserName']).get('NickName')
        try:
            replay_text = '{} recall message is {}'.format(msg['ActualNickName'], itchat.get_cache(key))
            info('group {}: {}: recall message is {}'.format(
                group_name, msg['ActualNickName'], replay_text))
        except KeyError as e:
            error('Keyerror {}'.format(str(e)))
            return

        return replay_text, msg['FromUserName']
        pass

    def match(self, msg, msg_type, sender_type) -> int:
        if msg_type == MessageType.Recall:
            return self.CERTAINLY
        else:
            return self.BACKGROUND
