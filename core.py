# coding=utf-8

import requests
import json
import configparser as cfg

class telegram_bot_api():
    
    def __init__(self, config_file):
        self.token = self.read_config(config_file)
        self.base = f"https://api.telegram.org/bot{self.token}/"

    def read_config(self, config_file):
        config = cfg.ConfigParser()
        config.read(config_file)
        return config.get("bot", "token")

    def send_chat_action(self, chat_id, action):
        url = f"{self.base}sendChatAction?chat_id={chat_id}&action={action}"
        try:
            requests.get(url)
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
    
    def reply_message(self, chat_id, message_content, reply_message_id):
        url = f"{self.base}sendMessage?chat_id={chat_id}&text={message_content}&reply_to_message_id={reply_message_id}&parse_mode=MarkdownV2"
        if message_content is not None:
            try:
                requests.get(url)
            except requests.exceptions.ConnectionError as error:
                print(f"couldn't connect to server, more imformation:\n{error}")
            except Exception as error:
                print(f"something went wrong, more imformation:\n{error}")
    
    def forward_message(self, chat_id, from_chat_id, message_id):
        url = f"{self.base}forwardMessage?chat_id={chat_id}&from_chat_id={from_chat_id}&message_id={message_id}"
        try:
            requests.get(url)
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")

    def send_message(self, chat_id, message_content):
        url = f"{self.base}sendMessage?chat_id={chat_id}&text={message_content}"
        if message_content is not None:
            try:
                requests.get(url)
            except requests.exceptions.ConnectionError as error:
                print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            except Exception as error:
                print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")

    def send_message_markdown(self, chat_id, message_content):
        url = f"{self.base}sendMessage?chat_id={chat_id}&text={message_content}&parse_mode=MarkdownV2"
        if message_content is not None:
            try:
                requests.get(url)
            except requests.exceptions.ConnectionError as error:
                print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            except Exception as error:
                print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")

    def send_sticker(self, chat_id, sticker_id):
        url = f"{self.base}sendSticker?chat_id={chat_id}&sticker={sticker_id}"
        if sticker_id is not None:
            try:
                requests.get(url)
            except requests.exceptions.ConnectionError as error:
                print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            except Exception as error:
                print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")

    def get_updates(self, offset):
        url = f"{self.base}getUpdates?timeout=100"
        if offset is not None:
            url = f"{url}&offset={int(offset) + 1}"
        try:
            r = requests.get(url)
            update = json.loads(r.content)
            return update
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")


    def get_me(self):
        url = f"{self.base}getMe"
        try:
            r = requests.get(url)
            bot_info = json.loads(r.content)
            return bot_info
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")