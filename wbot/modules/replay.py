# -*- encoding: utf-8 -*-
import pprint

from wbot.core.base import BaseModule
from wbot.core.types import SenderType


class ReplayModule(BaseModule):
    def handle(self, msg, msg_type, sender_type, background=False):
        pprint.pprint(msg)

    def match(self, msg, msg_type, sender_type) -> int:
        return -1
