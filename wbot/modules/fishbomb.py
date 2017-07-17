# -*- encoding: utf-8 -*-
import os
import pickle
import pprint

from wbot.core.base import BaseModule
from wbot.core.types import MessageType, SenderType
from wbot.core.wrapper import ItChatWrapper
from wbot.ext.log import debug
from wbot.utils import get_chatroom_name_by_username

BOMB_LOG = 'bomblog.obj'


class FishBombModule(BaseModule):

    @classmethod
    def init_from(cls, bot):
        return cls()

    CONFIG_PREFIX = "FISHBOMB"

    def __init__(self):
        if os.path.isfile(BOMB_LOG):
            with open(BOMB_LOG, 'rb') as f:
                self.log_set = pickle.load(f)
        else:
            self.log_set = set()

    def save_log(self):
        with open(BOMB_LOG, 'wb') as f:
            pickle.dump(self.log_set, f)

    def handle(self, msg, msg_type, sender_type, background=False, from_self=False):
        if background:
            if from_self:
                return
            username = msg['ActualNickName']
            to_user_name = msg['FromUserName']
            if username not in self.log_set:
                debug('%s Logged' % username)
                ItChatWrapper.send_msg('恭喜 @%s 冒泡成功！' % username, to_user_name)
                self.log_set.add(username)
                self.save_log()

    def match(self, msg, msg_type, sender_type, from_self=False) -> int:
        if sender_type is SenderType.Group:
            if get_chatroom_name_by_username(msg['FromUserName']) == 'PY Learning':
                return -1
        return 0
