# -*- encoding: utf-8 -*-
import errno
import os
import types

import itchat

from wbot.ext.log import debug, info


class BaseModule(object):
    CONFIG_PREFIX = "BASEMODULE"

    CERTAINLY = 100  # 一定匹配
    ALMOST = 80  # 几乎匹配
    LIKELY = 60  # 应该会匹配
    PERHAPS = 40  # 大概会匹配
    MAYBE = 20  # 有一定可能匹配
    IMPOSSIBLE = 0  # 绝不匹配
    BACKGROUND = -1  # 后台运行，通知该插件但不回复消息

    def handle(self, msg, msg_type, sender_type, background=False, from_self=False):
        """处理消息"""
        raise NotImplementedError

    def match(self, msg, msg_type, sender_type) -> int:
        """计算匹配程度
        100 - 完全匹配
        0   - 完全不匹配
        如果返回None则会当作0
        """
        raise NotImplementedError

    @classmethod
    def configs_from(cls, bot):
        """从Bot中读取所有以 CONFIG_PREFIX 为前缀的配置项目，去掉前缀、保存为字典返回"""
        result = dict()
        for key, value in bot.configs.items():
            if key.startswith(cls.CONFIG_PREFIX + '_'):
                result[key[len(cls.CONFIG_PREFIX) + 1:]] = value
        return result

    @classmethod
    def init_from(cls, bot):
        """从Bot配置中加载一个模块

        :return: 返回配置好的模块实例
        """
        raise NotImplementedError()

    @classmethod
    def register_from(cls, bot):
        """为Bot添加一个本类的模块实例

        :type bot: BaseBot
        :param bot: 要添加模块的机器人
        """
        module = cls.init_from(bot)
        bot.register(module)

    def after_login(self):
        """在Bot登录后调用"""
        pass

    def before_destory(self):
        """在程序结束前调用"""
        pass


class BotConfig(dict):
    def __init__(self, root_path, **kwargs):
        super(BotConfig, self).__init__(**kwargs)
        self.root_path = root_path

    def from_env(self, silent=False, env_name='WXBOT_CONFIG'):
        rv = os.environ.get(env_name)
        if not rv:
            if silent:
                return False
            raise RuntimeError('环境变量 %r 未设置，请设置环境变量指向配置文件' % env_name)
        return self.from_pyfile(rv, silent=silent)

    def from_pyfile(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, encoding='utf-8') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = '无法加载配置文件 (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        # if isinstance(obj, string_types):
        #     obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)


class BaseBot(object):
    """机器人基类

    Bot在处理消息时，会依次调用已注册模块的match函数，Match函数计算匹配度。随后选择匹配度最高的模块调用Handle方法处理消息
    """

    modules = []

    def __init__(self, config):
        self.configs = config
        self.user_name = None
        self.nick_name = None

    def run(self):
        """运行此Bot"""
        info("Bot Server start running...")
        try:
            itchat.auto_login(hotReload=True, enableCmdQR=2)
            self.after_login()
            itchat.run()
        except KeyboardInterrupt:
            info("KeyboardInterrupt occurred ...  Quitting, Bye.")
        self.before_destory()

    def handle_msg(self, msg, msg_type, sender_type):
        max_idx = 0
        max_match = 0
        background_list = []
        for idx, module in enumerate(self.modules):
            module_match = module.match(msg, msg_type, sender_type, from_self=msg['FromUserName'] == self.user_name)
            if module_match is None:
                module_match = 0
            if module_match > max_match:
                max_idx, max_match = idx, module_match
            if module_match < 0:
                background_list.append(idx)
        for idx in background_list:
            self.modules[idx].handle(msg, msg_type, sender_type, background=True,
                                     from_self=msg['FromUserName'] == self.user_name)
        if max_match == 0:
            return
        else:
            return self.modules[max_idx].handle(msg, msg_type, sender_type)

    def register(self, module: BaseModule):
        self.modules.append(module)

    def after_login(self):
        user = itchat.search_friends()
        self.user_name = user['UserName']
        self.nick_name = user['NickName']
        debug('Login username is: %s, nickname is: %s' % (self.user_name, self.nick_name))
        for module in self.modules:
            module.after_login()

    def before_destory(self):
        for module in self.modules:
            module.before_destory()
