# -*- encoding: utf-8 -*-
from . import logger


def init_ext(bot):
    logger.info('Initializing Extensions ...')
    logger.init_logging(bot)
