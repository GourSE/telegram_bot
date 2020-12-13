# coding=utf-8

import core
import json

class message():

    def __init__(self, get_updates_result):
        # define datas
        self.update_id =                        None
        self.content =                          None
        self.type =                             None
        self.is_group =                         None
        self.chat_title =                       None
        self.chat_id =                          None
        self.usr_first =                        None
        self.message_id =                       None
        self.usr_id =                           None
        self.is_reply =                         None
        self.reply_message_id =                 None
        self.reply_message_text =               None
        self.reply_message_is_text =            None
        self.reply_usr_id =                     None
        self.reply_usr_first =                  None
        self.reply_forward_usr_id =             None
        self.reply_forward_usr_first =          None
        self.reply_is_forward =                 None

        #check if fed is None type
        if get_updates_result is None:
            print('message_organizer: message fed is None type')
            exit()
        else:
            #get_updates_result = json.loads(str(get_updates_result))
            pass
        try:
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
        except:
            print("ERROR: can't get result")
            self.content = None
            return


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
        if chat_type == "group" or chat_type == "supergroup":
            self.is_group = True
        else:
            self.is_group = False

        if self.is_group:
            self.chat_title = fed_message["chat"]["title"]
            self.chat_id = fed_message["chat"]["id"]
        else:
            self.chat_title = fed_message["from"]["first_name"]
            self.chat_id = fed_message["from"]["id"]


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
            try:
                self.reply_message_text = fed_message["reply_to_message"]["text"]
                self.reply_message_is_text = True
            except:
                self.reply_message_text = None
                self.reply_message_is_text = False
            self.reply_usr_id = fed_message["reply_to_message"]["from"]["id"]
            self.reply_usr_first = fed_message["reply_to_message"]["from"]["first_name"]
            try:
                #check if message is forwared
                self.reply_forward_usr_id = fed_message["reply_to_message"]["forward_from"]["id"]
                self.reply_forward_usr_first = fed_message["reply_to_message"]["forward_from"]["first_name"]
                self.reply_is_forward = True
            except:
                self.reply_forward_usr_id = None
                self.reply_forward_usr_first = None
                self.reply_is_forward = False
        except:
            self.reply_forward_usr_id = None
            self.reply_message_is_text = False
            self.reply_forward_usr_first = None
            self.reply_message_id = None
            self.reply_usr_id = None
            self.reply_usr_first = None
            self.is_reply = False
            self.reply_is_forward = False
            self.reply_message_text = None
            

    #push expermental lol
    def message_pusher(self):
        print("push!")