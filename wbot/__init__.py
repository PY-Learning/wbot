# -*- encoding: utf-8 -*-
"""

@author: AZLisme <helloazl@icloud.com>
@time: 2017/3/20 下午3:08
"""

from wbot import ext, modules
from wbot.bot import WxBot
from wbot.core.base import BotConfig
from wbot.core.wrapper import ItChatWrapper
from wbot.ext import logger


def create_bot(root_path='.') -> WxBot:
    """创建一个默认机器人"""
    logger.info("Creating default bot.")
    logger.info("Loading Configuration...")
    config = BotConfig(root_path)
    config.from_pyfile('config.py', silent=True)
    config.from_env(silent=True)

    bot = WxBot(config)
    ext.init_ext(bot)
    modules.init_bot(bot)
    wrapper = ItChatWrapper(bot)
    wrapper.bind()
    return bot
