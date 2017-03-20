# -*- encoding: utf-8 -*-
"""

@author: AZLisme <helloazl@icloud.com>
@time: 2017/3/20 下午3:08
"""

from wbot import modules
from wbot.bot import WxBot
from wbot.core.wrapper import ItChatWrapper


def create_bot() -> WxBot:
    """创建一个默认机器人"""
    bot = WxBot()
    modules.init_bot(bot)
    wrapper = ItChatWrapper(bot)
    wrapper.bind()
    return bot
