# -*- encoding: utf-8 -*-
import pprint

from wbot.core.base import BaseModule
from wbot.core.types import MessageType, SenderType
from wbot.ext import logger
from wbot.utils import get_chatroom_name_by_username


class ReplayModule(BaseModule):
    @classmethod
    def init_from(cls, bot):
        return cls()

    CONFIG_PREFIX = "REPLAY"

    def handle(self, msg, msg_type, sender_type, background=False, from_self=False):
        if from_self:
            logger.debug(pprint.pformat(msg))
        if get_chatroom_name_by_username(msg['FromUserName']) == 'PY Learning':
            logger.debug("%s: %s" % (msg['ActualNickName'], msg['Content']))
        else:
            logger.debug("Message from: %s" % get_chatroom_name_by_username(msg['FromUserName']))

    def match(self, msg, msg_type, sender_type, from_self=False) -> int:
        if msg_type is MessageType.Text and sender_type is SenderType.Group:
            return -1
