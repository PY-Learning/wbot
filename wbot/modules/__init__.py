# -*- encoding: utf-8 -*-
"""

@author: AZLisme <helloazl@icloud.com>
@time: 2017/3/20 下午2:55
"""
import importlib
import os

from wbot.core.base import BaseBot, BaseModule
from wbot.ext.log import critical, debug, info


def init_bot(bot: BaseBot):
    load_installed('wbot/modules', bot.configs.get('PROJECT_ROOT'))
    info('Loading required module list ...')
    module_list = bot.configs.get("MODULE_LIST")
    debug('Load complete, modules: %s' % str(module_list))
    for module_name in module_list:
        m = None
        try:
            m = globals()[module_name]
        except KeyError:
            critical('Configured module [%s] not found, please check "/wbot/modules/__init__.py", '
                     'did you forget import such module?')
            exit(1)
        if m:
            debug('Registering module: %s ...' % module_name)
            m.register_from(bot)


def load_installed(path, project_root, base_module_name='wbot.modules'):
    """加载所有已经安装的模块

    :param path: 要扫描的路径（相对于项目目录）
    """
    info('Scanning Installed Modules...')
    install_path = os.path.join(project_root, path)
    dir_list = os.listdir(install_path)
    mods = list()
    for fname in dir_list:
        if os.path.isfile(os.path.join(path, fname)) and \
                fname.endswith('.py') and not fname.startswith('__'):

            key = fname[:-3]
            module_object = importlib.import_module('.'.join([base_module_name, key]))
            for attr in module_object.__dir__():
                ins = getattr(module_object, attr, None)
                if type(ins) is type and issubclass(ins, BaseModule) and (attr not in mods) and attr != 'BaseModule':
                    debug('Found Module: %s' % attr)
                    globals()[attr] = ins
                    mods.append(attr)
