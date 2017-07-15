# -*- coding: utf-8 -*-

##################
# General Config #
##################

LOGGER_FORMAT = "[%(levelname)s] %(asctime)s %(message)s"
LOGGER_LEVEL = "DEBUG"
LOGGER_DATEFMT = "%m/%d/%Y %I:%M:%S %p"
LOGGER_NAME = "wbot"

PROJECT_ROOT = '.'

# 在这里填写想要加载的模块列表(使用模块的类名)
MODULE_LIST = [
    "ReplayModule"
]

# 注册监听群名
# TODO <CI_Knight> NotImplemented
GROUP_LIST = [
    "PY Learning"
]

#################
# Tuling Module #
#################

TULING_API_KEY = "xxxx"
TULING_API_SECRET = "xxxxx"
TULING_API_URL = "http://www.tuling123.com/openapi/api"

##############
# Faq Module #
##############

FAQ_FRIEND_WELCOME = "你好"
FAQ_GROUP_INFO = "PY Learning"
FAQ_INVITE_KEY = "python"

######################
# Interpreter Module #
######################

# 解释器超时时间(s)
INTERPRETER_TIMEOUT = 3
# 解释返回值最大行数
INTERPRETER_MAXLINE = 10

#################
# Recall Module #
#################
RECALL_REDIS_HOST = "localhost"
RECALL_REDIS_PORT = 6379
RECALL_CACHE_BACKEND = "redis"
RECALL_CACHE_DIR = "cache"
RECALL_START_NOTIFY = None
RECALL_END_NOTIFY = None
