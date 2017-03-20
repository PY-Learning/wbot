# -*- encoding: utf-8 -*-
"""

@author: AZLisme <helloazl@icloud.com>
@time: 2017/3/20 下午2:55
"""

from wbot.core.base import BaseBot
from wbot.modules.faq import FaqModule
from wbot.modules.interpreter import InterpreterModule
from wbot.modules.recall import RecallModule
from wbot.modules.tuling import TuLingModule
from wbot.modules.replay import ReplayModule


def init_bot(bot: BaseBot):
    # FaqModule.register_from(bot)
    # InterpreterModule.register_from(bot)
    # RecallModule.register_from(bot)
    # TuLingModule.register_from(bot)
    # RecallModule.register_from(bot)
    ReplayModule.register_from(bot)
