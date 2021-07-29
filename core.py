# coding=utf-8

from organizer import chat
from colours import colour
import logging
import requests
import json
import os
import mimetypes
import configparser as cfg

class telegram_bot_api():
    
    def __init__(self, config_file):
        self.token = self.read_config(config_file)
        self.base = f"https://api.telegram.org/bot{self.token}/"

    def read_config(self, config_file):
        config = cfg.ConfigParser()
        config.read(config_file)
        token = config.get("bot", "token")

        if token == "bot token here" or token == "":
            while True:
                token = input(f"\
{colour.RED}You did not enter a bot token{colour.reset}\n\
please put your bot token in {colour.yellow}config.cfg{colour.reset} under {colour.blue}[bot] > [token]{colour.reset}\n\
The bot token you enter now will not be saved\n\
Enter bot token > $ ")
                if token == ":q":
                    print(f"{colour.GREEN}quit{colour.reset}\n")
                    os._exit(1)
                else:
                    break
        return token

    def check_ok(self, fed_json):
        ok = fed_json["ok"]
        if str(ok).lower() == "false":
            print(f"\nFrom {colour.BLUE}Telegram Bot API{colour.reset}:\n{colour.WARNING}{fed_json}{colour.reset}\n")
            return False
        else:
            return True

    def send_chat_action(self, chat_id, action):
        url = f"{self.base}sendChatAction?chat_id={chat_id}&action={action}"
        try:
            r = requests.get(url, timeout=5)
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

    def send_document(self, chat_id, document_location=None, document_id=None, text=None, is_markdown=False, reply_to_message_id=None):
        if document_location is not None:
            files = {'document': open(document_location, "rb")}
        elif document_id is None and document_location is None:
            print(f"{colour.WARNING}no file passed in(document_location, document_id){colour.reset}")
        elif document_id is not None and document_location is not None:
            print(f"{colour.WARNING}there can only be one file type(document_location, document_id){colour.reset}")
        else:
            pass

        if text is not None:
            caption = f"&caption={text}"
            if is_markdown:
                markdown = f"&parse_mode=MarkdownV2"
            else:
                markdown = ""
        else:
            caption = ""
            markdown = ""

        if reply_to_message_id is not None:
            reply_to_message = f"&reply_to_message_id={reply_to_message_id}"
        else:
            reply_to_message = ""

        if document_id is not None:
            document = f"&document={document_id}"
        else:
            document = ""

        url = f"{self.base}sendDocument?chat_id={chat_id}{document}{caption}{reply_to_message}{markdown}"

        try:
            if document_location is not None:
                r = requests.post(url, files = files, timeout=5)
            else:
                r = requests.get(url, timeout=5)

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

    def send_photo(self, chat_id, photo_location=None, photo_id=None, text=None, is_markdown=False, reply_to_message_id=None):
        if photo_location is not None:
            files = {'photo': open(photo_location, "rb")}
        elif photo_id is None and photo_location is None:
            print(f"{colour.WARNING}no file passed in(photo_location, photo_id){colour.reset}")
        elif photo_id is not None and photo_location is not None:
            print(f"{colour.WARNING}there can only be one file type(photo_location, photo_id){colour.reset}")
        else:
            pass

        if text is not None:
            caption = f"&caption={text}"
            if is_markdown:
                markdown = f"&parse_mode=MarkdownV2"
            else:
                markdown = ""
        else:
            caption = ""
            markdown = ""

        if reply_to_message_id is not None:
            reply_to_message = f"&reply_to_message_id={reply_to_message_id}"
        else:
            reply_to_message = ""

        if photo_id is not None:
            photo = f"&photo={photo_id}"
        else:
            photo = ""

        url = f"{self.base}sendPhoto?chat_id={chat_id}{photo}{caption}{reply_to_message}{markdown}"

        try:
            if photo_location is not None:
                r = requests.post(url, files = files, timeout=5)
            else:
                r = requests.get(url, timeout=5)

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

    def send_audio(self, chat_id, audio_location=None, audio_id=None, text=None, is_markdown=False, reply_to_message_id=None):
        if audio_location is not None:
            files = {'audio': open(audio_location, "rb")}
        elif audio_id is None and audio_location is None:
            print(f"{colour.WARNING}no file passed in(audio_location, audio_id){colour.reset}")
        elif audio_id is not None and audio_location is not None:
            print(f"{colour.WARNING}there can only be one file type(audio_location, audio_id){colour.reset}")
        else:
            pass

        if text is not None:
            caption = f"&caption={text}"
            if is_markdown:
                markdown = f"&parse_mode=MarkdownV2"
            else:
                markdown = ""
        else:
            caption = ""
            markdown = ""

        if reply_to_message_id is not None:
            reply_to_message = f"&reply_to_message_id={reply_to_message_id}"
        else:
            reply_to_message = ""

        if audio_id is not None:
            audio = f"&audio={audio_id}"
        else:
            audio = ""

        url = f"{self.base}sendAudio?chat_id={chat_id}{audio}{caption}{reply_to_message}{markdown}"

        try:
            if audio_location is not None:
                r = requests.post(url, files = files, timeout=5)
            else:
                r = requests.get(url, timeout=5)

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

    def send_video(self, chat_id, video_location=None, video_id=None, text=None, is_markdown=False, reply_to_message_id=None):
        if video_location is not None:
            files = {'video': open(video_location, "rb")}
        elif video_id is None and video_location is None:
            print(f"{colour.WARNING}no file passed in(video_location, video_id){colour.reset}")
        elif video_id is not None and video_location is not None:
            print(f"{colour.WARNING}there can only be one file type(video_location, video_id){colour.reset}")
        else:
            pass

        if text is not None:
            caption = f"&caption={text}"
            if is_markdown:
                markdown = f"&parse_mode=MarkdownV2"
            else:
                markdown = ""
        else:
            caption = ""
            markdown = ""

        if reply_to_message_id is not None:
            reply_to_message = f"&reply_to_message_id={reply_to_message_id}"
        else:
            reply_to_message = ""

        if video_id is not None:
            video = f"&video={video_id}"
        else:
            video = ""

        url = f"{self.base}sendVideo?chat_id={chat_id}{video}{caption}{reply_to_message}{markdown}"

        try:
            if video_location is not None:
                r = requests.post(url, files = files, timeout=5)
            else:
                r = requests.get(url, timeout=5)

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

    def send_animation(self, chat_id, animation_location=None, animation_id=None, text=None, is_markdown=False, reply_to_message_id=None):
        if animation_location is not None:
            files = {'animation': open(animation_location, "rb")}
        elif animation_id is None and animation_location is None:
            print(f"{colour.WARNING}no file passed in(animation_location, animation_id){colour.reset}")
        elif animation_id is not None and animation_location is not None:
            print(f"{colour.WARNING}there can only be one file type(animation_location, animation_id){colour.reset}")
        else:
            pass

        if text is not None:
            caption = f"&caption={text}"
            if is_markdown:
                markdown = f"&parse_mode=MarkdownV2"
            else:
                markdown = ""
        else:
            caption = ""
            markdown = ""

        if reply_to_message_id is not None:
            reply_to_message = f"&reply_to_message_id={reply_to_message_id}"
        else:
            reply_to_message = ""

        if animation_id is not None:
            animation = f"&animation={animation_id}"
        else:
            animation = ""

        url = f"{self.base}sendAnimation?chat_id={chat_id}{animation}{caption}{reply_to_message}{markdown}"

        try:
            if animation_location is not None:
                r = requests.post(url, files = files, timeout=5)
            else:
                r = requests.get(url, timeout=5)

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

    def send_message(self, chat_id, message_content, reply_to_message_id=None, is_markdown=False):
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
                r = requests.get(url, timeout=5)
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
            r = requests.get(url, timeout=5)
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


    def send_sticker(self, chat_id, sticker_id, reply_to_message_id=None):
        reply = ""
        
        if reply_to_message_id is not None:
            reply = f"&reply_to_message_id={reply_to_message_id}"
        else:
            pass

        url = f"{self.base}sendSticker?chat_id={chat_id}&sticker={sticker_id}{reply}"
        if sticker_id is not None:
            try:
                r = requests.get(url, timeout=5)
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

    def delete_message(self, chat_id, message_id):
        url = f"{self.base}deleteMessage?chat_id={chat_id}&message_id={message_id}"
        if message_id is not None and chat_id is not None:
            try:
                r = requests.get(url, timeout=5)
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
        url = f"{self.base}getUpdates?timeout=0"
        if offset is not None:
            url = f"{url}&offset={int(offset) + 1}"
        try:
            r = requests.get(url, timeout=5)
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

    def leave_chat(self, chat_id):
        url = f"{self.base}leaveChat?chat_id={chat_id}"
        if chat_id is not None:
            try:
                r = requests.get(url, timeout=5)
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

    def get_me(self):
        url = f"{self.base}getMe"
        try:
            r = requests.get(url, timeout=5)
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

    def get_chat(self, chat_id):
        url = f"{self.base}getChat?chat_id={chat_id}"
        try:
            r = requests.get(url, timeout=5)
            chat_info = json.loads(r.content)
            if self.check_ok(chat_info):
                return chat_info
            else:
                return False
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            return False
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
            return False

    def is_downloadable(self, url):
        h = requests.head(url, allow_redirects=True, timeout=5)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    def get_file(self, file_id):
        url = f"{self.base}getFile?file_id={file_id}"
        try:
            r = requests.get(url, timeout=5)
            output = json.loads(r.content)
            if self.check_ok(output):
                return output["result"]["file_path"]
            else:
                return False
        except requests.exceptions.ConnectionError as error:
            print(f"\ncouldn't connect to server, more imformation:\n\n{error}\n\n")
            return False
        except Exception as error:
            print(f"\nsomething went wrong, more imformation:\n\n{error}\n\n")
            return False

    def file_dl(self, file_id):
        path = self.get_file(file_id)

        url = f"https://api.telegram.org/file/bot{self.token}/{path}"

        file_name = url[int(url.rfind("/") + 1):]

        if self.is_downloadable(url):
            r = requests.get(url, allow_redirects=True, timeout=5)
            with open(file_name, "wb") as file:
                file.write(r.content)
                return file_name

        return None