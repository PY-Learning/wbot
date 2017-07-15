# -*- coding: utf-8 -*-
from wbot.core.base import BaseModule
from wbot.core.types import MessageType
from wbot.utils import MetaSingleton


class FaqModule(BaseModule):
    CONFIG_PREFIX = "FAQ"
    __metaclass__ = MetaSingleton

    @classmethod
    def init_from(cls, bot):
        config = cls.configs_from(bot)
        friend_welcome = config.get('FRIEND_WELCOME')
        group_info = config.get('GROUP_INFO')
        return cls(friend_welcome, group_info)

    def __init__(self, friend_welcome, group_info):
        super(FaqModule, self).__init__()
        self._friend_welcome = friend_welcome
        self._group_info = group_info

    @property
    def group_name(self):
        return self._group_info.get('name', 'PY Learning')

    @property
    def invite_key(self):
        return self._group_info.get('invite_key', 'PYTHON')

    def replay_welcome(self, is_group=False):
        if is_group: return None  # TODO group replay
        return self._friend_welcome

    def handle(self, msg, msg_type, sender_type, background=False):
        if msg_type == MessageType.Friends:
            return self.replay_welcome()

    def match(self, msg, msg_type, sender_type) -> int:
        if msg_type == MessageType.Friends:
            return self.ALMOST
