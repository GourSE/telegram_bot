# coding=utf-8

import requests
import json
import configparser as cfg


class telegram_bot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def send_message_markdown(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}&parse_mode=MarkdownV2".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)
    
    def reply_message(self, msg, chat_id, message_id):
        url = self.base + "sendMessage?chat_id={}&text={}&reply_to_message_id={}&parse_mode=MarkdownV2".format(chat_id, msg, message_id)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
    
    def get_me(self):
        url = self.base + "getMe"
        r = requests.get(url)
        return json.loads(r.content)
        