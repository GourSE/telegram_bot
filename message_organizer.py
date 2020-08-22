import core
#import time
import json
#from multiprocessing import Process
#import os

class message():

    def __init__(self, get_updates_result):

        #check if fed is None type
        if get_updates_result is None:
            print('message_organizer: message fed is None type')
            exit()
        else:
            #get_updates_result = json.loads(str(get_updates_result))
            pass

        try:
            #intended
            fed_message = get_updates_result["message"]

            #update ID
            self.update_id = get_updates_result["update_id"]

        except:
            #in case
            fed_message = get_updates_result["result"]["message"]

            #update ID
            self.update_id = get_updates_result["update_id"]

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
                file_unique_id = fed_message["sticker"]["file_id"]
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
            self.is_group = True
        else:
            self.is_group = False

        if self.is_group:
            self.chat_title = fed_message["chat"]["title"]
        else:
            pass


        #no last name, I don't want to check if there's a lastname or not
        #same as user ID, the t.me/ID one
        #probably will be included in the future
        self.usr_first = fed_message["from"]["first_name"]

        #message ID
        self.message_id = fed_message["message_id"]

        #userID
        self.usr_id = fed_message["from"]["id"]

        #check if the message is a reply_to
        try:
            self.is_reply = True
            self.reply_message_id = fed_message["reply_to_message"]["message_id"]
            self.reply_usr_id = fed_message["reply_to_message"]["from"]["id"]
            self.reply_usr_first = fed_message["reply_to_message"]["from"]["first_name"]
            try:
                #check if message is forwared
                self.reply_forward_usr_id = fed_message["reply_to_message"]["forward_from"]["id"]
                self.reply_forward_usr_first = fed_message["reply_to_message"]["forward_from"]["first_name"]
                self.reply_is_forward = True
            except:
                self.reply_is_forward = False
        except:
            self.is_reply = False
            self.reply_is_forward = False

    #push expermental lol
    def message_pusher(self):
        print("push!")