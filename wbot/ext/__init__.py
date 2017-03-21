# -*- encoding: utf-8 -*-
import logging

from wbot.ext.log import init_logging


def init_ext(bot):
    logging.log(logging.INFO, 'Initializing Extensions ...')
    init_logging(bot)
