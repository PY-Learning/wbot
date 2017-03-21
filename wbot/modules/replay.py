# -*- encoding: utf-8 -*-


from wbot.core.base import BaseModule
from wbot.ext.log import debug


class ReplayModule(BaseModule):
    @classmethod
    def init_from(cls, bot):
        return cls()

    CONFIG_PREFIX = "REPLAY"

    def handle(self, msg, msg_type, sender_type, background=False):
        debug(msg)

    def match(self, msg, msg_type, sender_type) -> int:
        return -1
