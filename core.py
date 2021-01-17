# coding=utf-8

from colours import colour
import logging
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
        token = config.get("bot", "token")

#         if token == "bot token here" or token == "":
#             token = input(f"\
# {colour.RED}You did not enter a bot token{colour.reset}\n\
# please put your bot token in {colour.yellow}config.cfg{colour.reset} under {colour.blue}[bot] > [token]{colour.reset}\n\
# The bot token you enter now will not be saved\n\
# Enter bot token: ")
#             return token

        return token

    def send_chat_action(self, chat_id, action):
        url = f"{self.base}sendChatAction?chat_id={chat_id}&action={action}"
        try:
            r = requests.get(url)
            fed = json.loads(r.content)
            if self.check_ok(fed):
                return True
            else:
                return False
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            return False
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
            return False

    # pass None to doc_id if you have a doc_location, pass None to doc_location if you have a doc_id
    def send_document(self, chat_id, doc_location, doc_id):
        if doc_location is None:
            pass
        elif doc_id is None and doc_location is None:
            print(f"{colour.WARNING}no file passed in(doc_location, doc_id){colour.reset}")
        elif doc_id is not None and doc_location is not None:
            print(f"{colour.WARNING}there can only be one file type(doc_location, doc_id){colour.reset}")
        else:
            files = {'document': open(doc_location)}

        try:
            if doc_location is not None:
                r = requests.post(f"{self.base}sendDocument?chat_id={chat_id}", files = files)
            else:
                r = requests.post(f"{self.base}sendDocument?chat_id={chat_id}&document={doc_id}")

            fed = json.loads(r.content)
            if self.check_ok(fed):
                return True
            else:
                return False
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            return False
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
            return False

    def send_message(self, chat_id, message_content, reply_to_message_id, is_markdown):
        if reply_to_message_id is not None:
            reply = f"&reply_to_message_id={reply_to_message_id}"
        else:
            reply = ""

        if is_markdown:
            markdown = "&parse_mode=MarkdownV2"
        else:
            markdown = ""

        url = f"{self.base}sendMessage?chat_id={chat_id}&text={message_content}{reply}{markdown}"
        
        if message_content is not None:
            try:
                r = requests.get(url)
                fed = json.loads(r.content)
                if self.check_ok(fed):
                    return True
                else:
                    return False
            except requests.exceptions.ConnectionError as error:
                print(f"couldn't connect to server, more imformation:\n{error}")
                return False
            except Exception as error:
                print(f"something went wrong, more imformation:\n{error}")
                return False

    def forward_message(self, chat_id, from_chat_id, message_id):
        url = f"{self.base}forwardMessage?chat_id={chat_id}&from_chat_id={from_chat_id}&message_id={message_id}"
        try:
            r = requests.get(url)
            fed = json.loads(r.content)
            if self.check_ok(fed):
                return True
            else:
                return False
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            return False
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
            return False

    def send_sticker(self, chat_id, sticker_id):
        url = f"{self.base}sendSticker?chat_id={chat_id}&sticker={sticker_id}"
        if sticker_id is not None:
            try:
                r = requests.get(url)
                fed = json.loads(r.content)
                if self.check_ok(fed):
                    return True
                else:
                    return False
            except requests.exceptions.ConnectionError as error:
                print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
                return False
            except Exception as error:
                print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
                return False

    def get_updates(self, offset):
        url = f"{self.base}getUpdates?timeout=100"
        if offset is not None:
            url = f"{url}&offset={int(offset) + 1}"
        try:
            r = requests.get(url)
            update = json.loads(r.content)
            if self.check_ok(update):
                return update
            else:
                return False
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            return False
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
            return False


    def get_me(self):
        url = f"{self.base}getMe"
        try:
            r = requests.get(url)
            bot_info = json.loads(r.content)
            if self.check_ok(bot_info):
                return bot_info
            else:
                return False
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            return False
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
            return False
        
    def check_ok(self, fed_json):
        ok = fed_json["ok"]
        # print(fed_json)
        if str(ok).lower() == "false":
            print(f"\nFrom {colour.BLUE}Telegram Bot API{colour.reset}:\n{colour.WARNING}{fed_json}{colour.reset}\n")
            return False
        else:
            return True