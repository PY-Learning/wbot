# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue

# 命令执行的超时时间(s)
DEFAULT_TIMEOUT = 1
MAX_LINE = 10


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

    def __init__(self, cmd):
        Process.__init__(self)
        self.cmd = cmd
        self.queue = Queue()

    def run(self):
        import sys as __sys
        for item in self.__BLOCK_LIST__:
            del __sys.modules[item]
        text_area = TextArea()
        __sys.stdout = text_area
        del __sys
        try:
            exec(self.cmd, dict(open=fake_open), dict())
        except ImportError:
            text_area.write("找不到或者调用了禁止的库, 不要使坏哦～")
        except Exception as e:
            text_area.write("执行错误：{}".format(e))

        result = ''.join([''.join(text) for text in text_area.buffer])
        if len(result.split('\n')) >= MAX_LINE:
            result = '\n'.join(result.split('\n')[:MAX_LINE])
            result += '\n 行数超出或等于限制，已被隐藏'

        self.queue.put(result)


def async_run(cmd):
    process = PythonProcess(cmd)
    process.start()
    process.join(timeout=DEFAULT_TIMEOUT)
    if process.exitcode is None:
        process.terminate()
        return "运行超时，中止运行"
    else:
        return process.queue.get(True, DEFAULT_TIMEOUT)


class Interpreter(object):
    PY_SYMBLOE = '#'

    def __init___(self, *args, **kwargs):
        super(Interpreter, self).__init__()

    @staticmethod
    def run_py_cmd(cmd):
        cmd = cmd.strip()
        if not cmd: return 'NULL'

        try:
            # eval("eval('__import__(\"os\")')", {'__builtins__':__builtins__, "__import__": None})))"
            return async_run(cmd)
        except:
            return '出现未知执行错误'
