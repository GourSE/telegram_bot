import core
#import time
import json
#from multiprocessing import Process
#import os

bot = core.telegram_bot_api("config.cfg")
class message():

    #message, starting from "result" in getUpdate json
    #only one message sent at a time

    def __init__(self, get_updates_result):
        fed_message = get_updates_result["message"]

        #try to get message content in json
        #doing it one by one with try except
        #starting with the most common file type to the less common one
        #only text, sticker, photo supported
        #there's probably a better solution I don't know

        try:
            self.content = fed_message["text"]
            self.type = "text"
        except:
            try:
                file_unique_id = fed_message["sticker"]["file_unique_id"]
                self.content = f"sticker: {file_unique_id}"
                self.type = "sticker"
            except:
                try:
                    file_unique_id = fed_message["photo"][file_unique_id]
                    self.content = f"photo, {file_unique_id}"
                    self.type = "photo"
                except:
                    self.content = None
                    self.type = None

        #chat
        chat_type = fed_message["chat"]["type"]
        if chat_type == "group":
            is_group = True
        else:
            is_group = False

        if is_group:
            self.chat_title = fed_message["chat"]["title"]
        else:
            pass

        #message ID
        self.message_id = fed_message["message_id"]

        #userID
        self.usr_id = fed_message["from"]["id"]

        #no last name, I don't want to check if there's a lastname or not
        #same as user ID, the t.me/ID one
        #probably will be included in the future
        self.usr_first = fed_message["from"]["first_name"]

        #check if the message is a reply_to
        try:
            self.is_reply = True
            self.reply_message_id = fed_message["message_id"]
            self.reply_usr_id = fed_message["from"]["id"]
            self.reply_usr_first = fed_message["from"]["first_name"]
        except:
            self.is_reply = False

    #push expermental lol
    def message_pusher(self):
        print("push!")