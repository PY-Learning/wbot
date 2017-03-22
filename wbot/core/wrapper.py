# -*- encoding: utf-8 -*-

import itchat
from wbot.core.base import BaseBot
from wbot.core.types import MessageType, SenderType


class ItChatWrapper(object):
    """对Itchat的调用装饰器接口做一层封装，转发到Bot的消息路由中, 并封装其他的静态API"""
    bot = None

    def __init__(self, bot: BaseBot):
        self.bot = bot

    def _handle_group(self, msg):
        return self.bot.handle_msg(msg, MessageType(msg['Type']), SenderType.Group)

    def _handle_friends(self, msg):
        return self.bot.handle_msg(msg, MessageType(msg['Type']), SenderType.Friends)

    def _handle_mp(self, msg):
        return self.bot.handle_msg(msg, MessageType(msg['Type']), SenderType.Mp)

    def bind(self):
        all_type_list = [i for i in MessageType.__members__]
        itchat.msg_register(all_type_list, isFriendChat=True)(self._handle_friends)
        itchat.msg_register(all_type_list, isGroupChat=True)(self._handle_group)
        itchat.msg_register(all_type_list, isMpChat=True)(self._handle_mp)

    @staticmethod
    def search_chatroom():
        #  TODO: ItChatWrapper search_chatroom  
        pass

    @staticmethod
    def search_friends(name=None, user_name=None, remark_name=None, nick_name=None, wechat_account=None):
        return itchat.search_friends(name, user_name, remark_name, nick_name, wechat_account)

    @staticmethod
    def search_chatrooms(name=None, user_name=None):
        return itchat.search_chatrooms(name, user_name)

    @staticmethod
    def search_mps(name=None, user_name=None):
        itchat.send_raw_msg
        return itchat.search_mps(name, user_name)

    @staticmethod
    def update_chatroom(user_name, detailed_member=False):
        ''' update chatroom
            for chatroom contact
                - a chatroom contact need updating to be detailed
                - detailed means members, encryid, etc
                - auto updating of heart loop is a more detailed updating
                    - member uin will also be filled
                - once called, updated info will be stored
            for options
                - user_name: 'user_name' key of chatroom or a list of it
                - detailed_member: whether to get members of contact
            it is defined in components/contact.py
        '''
        return itchat.update_chatroom(user_name, detailed_member)

    @staticmethod
    def update_friend(user_name):
        ''' update chatroom
            for friend contact
                - once called, updated info will be stored
            for options
                - user_name: 'user_name' key of a friend or a list of it
            it is defined in components/contact.py
        '''
        raise NotImplementedError("This method has not been implement yet.")

    @staticmethod
    def get_contact(update=False):
        ''' fetch part of contact
            for part
                - all the massive platforms and friends are fetched
                - if update, only starred chatrooms are fetched
            for options
                - update: if not set, local value will be returned
            for results
                - chatroomList will be returned
            it is defined in components/contact.py
        '''
        return itchat.get_contract(update)

    @staticmethod
    def get_friends(update=False):
        ''' fetch friends list
            for options
                - update: if not set, local value will be returned
            for results
                - a list of friends' info dicts will be returned
            it is defined in components/contact.py
        '''
        return itchat.get_friends(update)

    @staticmethod
    def get_chatrooms(update=False, contact_only=False):
        ''' fetch chatrooms list
            for options
                - update: if not set, local value will be returned
                - contact_only: if set, only starred chatrooms will be returned
            for results
                - a list of chatrooms' info dicts will be returned
            it is defined in components/contact.py
        '''
        return itchat.get_chatrooms(update)

    @staticmethod
    def get_mps(update=False):
        ''' fetch massive platforms list
            for options
                - update: if not set, local value will be returned
            for results
                - a list of platforms' info dicts will be returned
            it is defined in components/contact.py
        '''
        return itchat.get_mps(update)

    @staticmethod
    def set_alias(user_name, alias):
        ''' set alias for a friend
            for options
                - user_name: 'user_name' key of info dict
                - alias: new alias
            it is defined in components/contact.py
        '''
        return itchat.set_alias(user_name, alias)

    @staticmethod
    def set_pinned(user_name, is_pinned=True):
        ''' set pinned for a friend or a chatroom
            for options
                - user_name: 'user_name' key of info dict
                - isPinned: whether to pin
            it is defined in components/contact.py
        '''
        return itchat.set_pinned(user_name, is_pinned)

    @staticmethod
    def add_friend(user_name, status=2, verify_content='', auto_update=True):
        ''' add a friend or accept a friend
            for options
                - user_name: 'user_name' for friend's info dict
                - status:
                    - for adding status should be 2
                    - for accepting status should be 3
                - ticket: greeting message
                - userInfo: friend's other info for adding into local storage
            it is defined in components/contact.py
        '''
        return itchat.add_friend(user_name, status, verify_content, auto_update)

    @staticmethod
    def get_head_img(user_name=None, chatroom_user_name=None, pic_dir=None):
        ''' place for docs
            for options
                - if you want to get chatroom header: only set chatroom_user_name
                - if you want to get friend header: only set user_name
                - if you want to get chatroom member header: set both
            it is defined in components/contact.py
        '''
        return itchat.get_head_img(user_name, chatroom_user_name, pic_dir)

    @staticmethod
    def create_chatroom(member_list, topic=''):
        ''' create a chatroom
            for creating
                - its calling frequency is strictly limited
            for options
                - member_list: list of member info dict
                - topic: topic of new chatroom
            it is defined in components/contact.py
        '''
        return itchat.create_chatroom(member_list, topic)

    @staticmethod
    def set_chatroom_name(chatroom_user_name, name):
        ''' set chatroom name
            for setting
                - it makes an updating of chatroom
                - which means detailed info will be returned in heart loop
            for options
                - chatroom_user_name: 'user_name' key of chatroom info dict
                - name: new chatroom name
            it is defined in components/contact.py
        '''
        return itchat.set_chatroom_name(chatroom_user_name, name)

    @staticmethod
    def delete_member_from_chatroom(chatroom_user_name, member_list):
        ''' deletes members from chatroom
            for deleting
                - you can't delete yourself
                - if so, no one will be deleted
                - strict-limited frequency
            for options
                - chatroom_user_name: 'user_name' key of chatroom info dict
                - member_list: list of members' info dict
            it is defined in components/contact.py
        '''
        return itchat.delete_member_from_chatroom(chatroom_user_name, member_list)

    @staticmethod
    def add_member_into_chatroom(chatroom_user_name, member_list,
                                 use_invitation=False):
        ''' add members into chatroom
            for adding
                - you can't add yourself or member already in chatroom
                - if so, no one will be added
                - if member will over 40 after adding, invitation must be used
                - strict-limited frequency
            for options
                - chatroom_user_name: 'user_name' key of chatroom info dict
                - member_list: list of members' info dict
                - use_invitation: if invitation is not required, set this to use
            it is defined in components/contact.py
        '''
        return itchat.add_member_into_chatroom(chatroom_user_name, member_list, use_invitation)

    @staticmethod
    def send_raw_msg(msg_type, content, to_user_name):
        ''' many messages are sent in a common way
            for demo
                .. code:: python

                    @itchat.msg_register(itchat.content.CARD)
                    def reply(msg):
                        itchat.send_raw_msg(msg['msg_type'], msg['Content'], msg['Fromuser_name'])

            there are some little tricks here, you may discover them yourself
            but remember they are tricks
            it is defined in components/messages.py
        '''
        raise NotImplementedError()

    @staticmethod
    def send_msg(msg='Test Message', to_user_name=None):
        ''' send plain text message
            for options
                - msg: should be unicode if there's non-ascii words in msg
                - to_user_name: 'user_name' key of friend dict
            it is defined in components/messages.py
        '''
        return itchat.send_msg(msg, to_user_name)

    @staticmethod
    def upload_file(file_dir, is_picture=False, is_video=False):
        ''' upload file to server and get media_id
            for options
                - file_dir: dir for file ready for upload
                - is_picture: whether file is a picture
                - is_video: whether file is a video
            for return values
                will return a ReturnValue
                if succeeded, media_id is in r['media_id']
            it is defined in components/messages.py
        '''
        raise NotImplementedError()

    @staticmethod
    def send_file(file_dir, to_user_name=None, media_id=None):
        ''' send attachment
            for options
                - file_dir: dir for file ready for upload
                - media_id: media_id for file.
                    - if set, file will not be uploaded twice
                - to_user_name: 'user_name' key of friend dict
            it is defined in components/messages.py
        '''
        return itchat.send_file(file_dir, to_user_name)

    @staticmethod
    def send_image(file_dir, to_user_name=None, media_id=None):
        ''' send image
            for options
                - file_dir: dir for file ready for upload
                    - if it's a gif, name it like 'xx.gif'
                - media_id: media_id for file.
                    - if set, file will not be uploaded twice
                - to_user_name: 'user_name' key of friend dict
            it is defined in components/messages.py
        '''
        return itchat.send_image(file_dir, to_user_name, media_id)

    @staticmethod
    def send_video(file_dir=None, to_user_name=None, media_id=None):
        ''' send video
            for options
                - file_dir: dir for file ready for upload
                    - if media_id is set, it's unnecessary to set file_dir
                - media_id: media_id for file.
                    - if set, file will not be uploaded twice
                - to_user_name: 'user_name' key of friend dict
            it is defined in components/messages.py
        '''
        return itchat.send_video(file_dir, to_user_name)

    @staticmethod
    def send(msg, to_user_name=None, media_id=None):
        ''' wrapped function for all the sending functions
            for options
                - msg: message starts with different string indicates different type
                    - list of type string: ['@fil@', '@img@', '@msg@', '@vid@']
                    - they are for file, image, plain text, video
                    - if none of them matches, it will be sent like plain text
                - to_user_name: 'user_name' key of friend dict
                - media_id: if set, uploading will not be repeated
            it is defined in components/messages.py
        '''
        return itchat.send(msg, to_user_name)
