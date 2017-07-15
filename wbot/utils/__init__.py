# -*- encoding: utf-8 -*-

from .singleton import MetaSingleton

from wbot.core.wrapper import ItChatWrapper


def get_chatroom_name_by_username(username: str) -> str:
    """将群的UserName转化成群昵称

    例如：PY Learning 的群 UserName 为 @@abcdef1234567890
    转化后输出 PY Learning
    """
    return ItChatWrapper.search_chatrooms(user_name=username).get('NickName')
