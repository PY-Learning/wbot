# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue

from wbot.core.base import BaseModule
from wbot.core.types import MessageType, SenderType


class TextArea(object):
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)


def fake_open(*args, **kwargs):
    raise Exception("访问文件IO是禁止的哦")


class PythonProcess(Process):
    # 禁止调用的库名单
    __BLOCK_LIST__ = ['sys', 'os', 'requests', 'socket', 'urllib', 'subprocess', 'codecs']

    def __init__(self, cmd, maxline):
        Process.__init__(self)
        self.cmd = cmd
        self.maxline = maxline
        self.queue = Queue()

    def run(self):
        import sys
        for item in self.__BLOCK_LIST__:
            sys.modules[item] = None

        text_area = TextArea()
        sys.stdout = text_area
        try:
            exec(self.cmd, dict(open=fake_open), dict())
        except ImportError:
            text_area.write("找不到或者调用了禁止的库, 不要使坏哦～")
        except Exception as e:
            text_area.write("执行错误：{}".format(e))
        finally:
            del sys

        result = ''.join([''.join(text) for text in text_area.buffer])
        if len(result.split('\n')) >= self.maxline:
            result = '\n'.join(result.split('\n')[:self.maxline])
            result += '\n 行数超出或等于限制，已被隐藏'

        self.queue.put(result)


def async_run(cmd, timeout, maxline):
    process = PythonProcess(cmd, maxline)
    process.start()
    process.join(timeout=timeout)
    if process.exitcode is None:
        process.terminate()
        return "运行超时，中止运行"
    else:
        return process.queue.get(True, timeout)


class InterpreterModule(BaseModule):
    PY_SYMBOL = '#'
    CONFIG_PREFIX = "INTERPRETER"

    def __init__(self, timeout=3, maxline=10):
        self.timeout = timeout
        self.maxline = maxline

    @classmethod
    def init_from(cls, bot):
        config = cls.configs_from(bot)
        timeout = config['TIMEOUT']
        maxline = config['MAXLINE']
        return cls(timeout=timeout, maxline=maxline)

    def __init___(self, *args, **kwargs):
        super(InterpreterModule, self).__init__()

    def run_py_cmd(self, cmd):
        cmd = cmd.strip()
        if not cmd: return 'NULL'

        try:
            # eval("eval('__import__(\"os\")')", {'__builtins__':__builtins__, "__import__": None})))"
            return async_run(cmd, self.timeout, self.maxline)
        except:
            return '出现未知执行错误'

    def handle(self, msg, msg_type, sender_type, background=False):
        self.run_py_cmd(msg['Text'][1:])

    def match(self, msg, msg_type, sender_type) -> int:
        if msg_type in MessageType.Text \
                and sender_type in (SenderType.Friends, SenderType.Group) \
                and msg['Text'].startswith(self.PY_SYMBOL):
            return self.CERTAINLY
