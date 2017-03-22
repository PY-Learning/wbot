# -*- encoding: utf-8 -*-
import hashlib
import html
import os

import redis
import xmltodict

from wbot.core.base import BaseModule
from wbot.core.types import MessageType, SenderType
from wbot.core.wrapper import ItChatWrapper
from wbot.utils import get_chatroom_name_by_username


def save_to(data: bytes, name: str, dirs='cache'):
    """保存至指定文件夹"""
    path = os.path.join(dirs, name)
    if len(data) < 10:
        return
    if os.path.isfile(path):
        return
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as f:
        f.write(data)


def cal_md5(data: bytes):
    md5 = hashlib.md5(data)
    return md5.hexdigest()


def is_recall_message(msg, msg_type):
    """判断消息是否是撤回消息"""
    return msg['MsgType'] == 10002


def gen_key(msg, msg_type):
    """计算存储Key"""
    if is_recall_message(msg, msg_type):
        content = html.unescape(msg['Content'])
        content = xmltodict.parse(content)
        msgid = content['sysmsg']['revokemsg']['msgid']
        return '{}:{}'.format(msg['FromUserName'], msgid)
    else:
        return '{}:{}'.format(msg['FromUserName'], msg['MsgId'])


class RecallModule(BaseModule):
    CONFIG_PREFIX = "RECALL"

    def __init__(self, redis, cache_dir='cache'):
        self.redis = redis
        self.user_name = None
        self.nick_name = None
        self.cache_dir = cache_dir

    @classmethod
    def init_from(cls, bot):
        host = bot.configs.get('REDIS_HOST', 'localhost')
        port = bot.configs.get('REDIS_PORT', 6379)
        redis_client = redis.Redis(host=host, port=port)
        return cls(redis_client)

    def store_msg(self, msg, msg_type, sender_type):
        """存储消息

        支持文本、图片、视频、录音、附件的存储
        """
        key = gen_key(msg, msg_type)
        typ = msg_type.value
        if msg_type is MessageType.Text:
            content = msg['Content']
        elif msg_type in (MessageType.Picture, MessageType.Video, MessageType.Recording, MessageType.Attachment):
            data = msg['Text']()  # type: bytes
            filename = msg['FileName']
            _, extension = os.path.splitext(filename)
            if msg_type is MessageType.Attachment:
                saved_name = os.path.join(cal_md5(data), filename)
            else:
                saved_name = cal_md5(data) + extension
            save_to(data, saved_name, self.cache_dir)
            content = saved_name
        elif msg_type is MessageType.Sharing:
            content = content = "{location}。链接地址：{url}。".format(location=msg["Text"], url=msg['Url'])
        elif msg_type is MessageType.Map:
            content = "{location}。腾讯地图链接：{url}。".format(location=msg["Content"].split('\n')[0][:-1], url=msg['Url'])
        else:
            return
        self.redis.set('WXBOTTYPE' + key, typ, 300)
        self.redis.set('WXBOTCNTN' + key, content, 300)

    def resend(self, msg, msg_type, sender_type):
        """重发消息"""
        if is_recall_message(msg, msg_type):
            key = gen_key(msg, msg_type)
            content = self.redis.get('WXBOTCNTN' + key).decode('utf-8')
            typ = self.redis.get('WXBOTTYPE' + key).decode('utf-8')
            username = msg['NickName'] if sender_type is SenderType.Friends else msg['ActualNickName']
            to_user_name = msg['FromUserName']
            if content:
                if typ == 'Text':
                    ItChatWrapper.send_msg("{username} 撤回消息：\n\n{content}".format(username=username, content=content),
                                           to_user_name)
                elif typ in ("Picture", "Video", "Recording", "Attachment"):
                    cn_type = {'Picture': '图片', 'Video': '视频', 'Recording': '录音', 'Attachment': '附件'}[typ]
                    send_meth = {'Picture': ItChatWrapper.send_image, 'Video': ItChatWrapper.send_video,
                                 'Recording': ItChatWrapper.send_file, 'Attachment': ItChatWrapper.send_file}[typ]

                    content_path = os.path.join(self.cache_dir, content)
                    if os.path.isfile(content_path):
                        ItChatWrapper.send_msg("{username} 撤回{typ}:".format(username=username, typ=cn_type),
                                               to_user_name)
                        send_meth(content_path, to_user_name)
                    else:
                        ItChatWrapper.send_msg(
                            "{username} 撤回一个{typ}，但是文件不存在无法恢复。".format(username=username, typ=cn_type), to_user_name)
                elif typ == "Sharing":
                    ItChatWrapper.send_msg(
                        "{username} 撤回分享链接：{content}".format(username=username, content=content), to_user_name)
                elif typ == "Map":
                    ItChatWrapper.send_msg(
                        "{username} 撤回地图位置：{content}".format(username=username, content=content), to_user_name)
                else:
                    pass

    def handle(self, msg, msg_type, sender_type, background=False, from_self=False):
        if from_self:
            return
        if background:
            self.store_msg(msg, msg_type, sender_type)
        else:
            self.resend(msg, msg_type, sender_type)

    def match(self, msg, msg_type, sender_type, from_self=False) -> int:
        if from_self:
            return 0

        if sender_type is SenderType.Group:
            if msg_type not in (MessageType.Text, MessageType.Video, MessageType.Picture, MessageType.Recording,
                                MessageType.Attachment, MessageType.Map, MessageType.Sharing, MessageType.Note):
                return
            group_name = get_chatroom_name_by_username(msg['FromUserName'])
            if group_name in ('PY Learning', 'test1'):

                if is_recall_message(msg, msg_type):
                    return self.CERTAINLY
                else:
                    return self.BACKGROUND
