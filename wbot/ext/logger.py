# -*- encoding: utf-8 -*-
import logging
import sys

_logger = None

#  在加载Logging配置之前首先使用最简模式的Logger
logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(asctime)s %(name)s:%(message)s",
                    datefmt="%H:%M:%S", stream=sys.stdout)


def init_logging(bot):
    global _logger
    fmt = bot.configs.get('LOGGER_FORMAT', "[%(levelname)s] %(asctime)s %(message)s")
    level = bot.configs.get('LOGGER_LEVEL', "INFO")
    datefmt = bot.configs.get('LOGGER_DATEFMT', '%m/%d/%Y %I:%M:%S %p')
    logger_name = bot.configs.get('LOGGER_NAME', 'wbot')
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    handler.setLevel(level)
    _logger = logging.Logger(logger_name)
    _logger.addHandler(handler)


def log(level, msg, *args, **kwargs):
    if _logger:
        _logger.log(level, msg, *args, **kwargs)
    else:
        logging.log(level, msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    log(logging.DEBUG, msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    log(logging.INFO, msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    log(logging.WARNING, msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    log(logging.ERROR, msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    log(logging.CRITICAL, msg, *args, **kwargs)
