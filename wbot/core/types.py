# -*- encoding: utf-8 -*-
"""封装 ItChat 的基本类型

"""
from enum import Enum

from itchat.content import ATTACHMENT, CARD, FRIENDS, MAP, NOTE, PICTURE, RECORDING, SHARING, TEXT, VIDEO, SYSTEM


class MessageType(Enum):
    Text = TEXT
    Map = MAP
    Card = CARD
    Note = NOTE
    Sharing = SHARING
    Picture = PICTURE
    Recording = RECORDING
    Attachment = ATTACHMENT
    Video = VIDEO
    Friends = FRIENDS
    System = SYSTEM


class SenderType(Enum):
    Group = 'Group'
    Friends = 'Friends'
    Mp = "Mp"
