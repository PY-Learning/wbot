# -*- encoding: utf-8 -*-

import itchat
from wbot.core.base import BaseBot
from wbot.core.types import MessageType, SenderType


class ItChatWrapper(object):
    """对Itchat的调用装饰器接口做一层封装，转发到Bot的消息路由中, 并封装其他的静态API"""
    bot = None

    def __init__(self, bot: BaseBot):
        self.bot = bot

    def _handle_group(self, msg):
        return self.bot.handle_msg(msg, MessageType(msg['Type']), SenderType.Group)

    def _handle_friends(self, msg):
        return self.bot.handle_msg(msg, MessageType(msg['Type']), SenderType.Friends)

    def _handle_mp(self, msg):
        return self.bot.handle_msg(msg, MessageType(msg['Type']), SenderType.Mp)

    def bind(self):
        all_type_list = [i for i in MessageType.__members__]
        itchat.msg_register(all_type_list, isFriendChat=True)(self._handle_friends)
        itchat.msg_register(all_type_list, isGroupChat=True)(self._handle_group)
        itchat.msg_register(all_type_list, isMpChat=True)(self._handle_mp)
