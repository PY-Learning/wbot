# -*- encoding: utf-8 -*-

import itchat


class BaseModule(object):
    CONFIG_PREFIX = "BASEMODULE"

    CERTAINLY = 100  # 一定匹配
    ALMOST = 80  # 几乎匹配
    LIKELY = 60  # 应该会匹配
    PERHAPS = 40  # 大概会匹配
    MAYBE = 20  # 有一定可能匹配
    IMPOSSIBLE = 0  # 绝不匹配
    BACKGROUND = -1  # 后台运行，通知该插件但不回复消息

    def handle(self, msg, msg_type, sender_type, background=False):
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
        """从Bot中读取所有以 CONFIG_PREFIX 为前缀的配置项目，去掉前缀、保存为字典、并小写化Key返回"""
        result = dict()
        for key, value in bot.configs.items():
            if key.startswith(cls.CONFIG_PREFIX + '_'):
                result[key[len(cls.CONFIG_PREFIX) + 1:].lower()] = value
        return result

    @classmethod
    def init_from(cls, bot):
        """从Bot配置中加载一个模块"""
        configs = cls.configs_from(bot)
        return cls(**configs)

    @classmethod
    def register_from(cls, bot):
        """为Bot添加一个本类的模块实例

        :type bot: BaseBot
        :param bot: 要添加模块的机器人
        """
        module = cls.init_from(bot)
        bot.register(module)


class BaseBot(object):
    """机器人基类

    Bot在处理消息时，会依次调用已注册模块的match函数，Match函数计算匹配度。随后选择匹配度最高的模块调用Handle方法处理消息
    """

    modules = []
    configs = dict()

    def __init__(self):
        pass

    def run(self):
        """运行此Bot"""
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        itchat.run()

    def handle_msg(self, msg, msg_type, sender_type):
        max_idx = 0
        max_match = 0
        background_list = []
        for idx, module in enumerate(self.modules):
            module_match = module.match(msg, msg_type, sender_type) or 0
            if module_match > max_match:
                max_idx, max_match = idx, module_match
            if module_match < 0:
                background_list.append(idx)
        for idx in background_list:
            self.modules[idx].handle(msg, msg_type, sender_type, background=True)
        if max_match == 0:
            return
        else:
            return self.modules[max_idx].handle(msg, msg_type, sender_type)

    def register(self, module: BaseModule):
        self.modules.append(module)

    def from_dict(self, d):
        #  TODO: BaseBot from_dict
        pass

    def from_env(self, env_name='WXBOT_CONFIG'):
        #  TODO: BaseBot from_env
        pass
