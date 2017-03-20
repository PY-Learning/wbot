# -*- coding: utf-8 -*-
from wbot.core.base import BaseModule
from wbot.core.singleton import MetaSingleton
from wbot.core.types import MessageType


class FaqModule(BaseModule):
    __metaclass__ = MetaSingleton

    def __init__(self, *args, **kwargs):
        super(FaqModule, self).__init__()
        self._friend_welcome = kwargs.get('friend_welcome', '')
        self._group_info = kwargs.get('group_info', {})

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
