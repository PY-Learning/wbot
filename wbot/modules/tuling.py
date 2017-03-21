# -*- coding: utf-8 -*-

import requests

from wbot.core.base import BaseModule
from wbot.core.singleton import MetaSingleton
from wbot.core.types import MessageType


class TuLingModule(BaseModule):
    """
    Tuling robot http://www.tuling123.com
    Doc http://www.tuling123.com/help/h_cent_webapi.jhtml
    """
    CONFIG_PREFIX = "TULING"
    __metaclass__ = MetaSingleton

    SUB_TYPE_TEXT = 100000

    def __init__(self, api_key, api_secret, api_url):
        super(TuLingModule, self).__init__()
        self._api_key = api_key
        self._api_secret = api_secret
        self._api_url = api_url
        assert self._api_key and self._api_secret, \
            'tuling key or secret is None'

    @classmethod
    def init_from(cls, bot):
        configs = cls.configs_from(bot)
        api_key = configs.get("API_KEY")
        api_secret = configs.get("API_SECRET")
        api_url = configs.get("API_URL")
        return cls(api_key, api_secret, api_url)

    def _post(self, data):
        response = requests.post(url=self._api_url, data=data)
        if response.status_code is not 200:
            return None
        return response.json()

    def replay_text(self, info, userid=None):
        if not info.strip():
            return '你要说些什么?'

        data = {
            'key': self._api_key,
            'info': info
        }
        if userid: data['userid'] = userid
        return_dict = self._post(data)
        # TODO news and urls type
        if return_dict['code'] == TuLingModule.SUB_TYPE_TEXT:
            return return_dict['text']

        return None

    def match(self, msg, msg_type, sender_type):
        if msg_type in [MessageType.Text] and msg['isAt']:
            return 1  # 最低的优先级

    def handle(self, msg, msg_type, sender_type, background=False):
        return self.replay_text(msg['Text'])
