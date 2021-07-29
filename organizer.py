# coding=utf-8

import json

class message():

    def __init__(self, get_updates_result):
        # define datas
        self.update_id =                        None
        self.content =                          None
        self.file_unique_id =                   None
        self.type =                             None
        self.is_group =                         None
        self.chat_title =                       None
        self.chat_id =                          None
        self.usr_first =                        None
        self.usr_last =                         None
        self.usr_name =                         None
        self.message_id =                       None
        self.usr_id =                           None
        self.is_reply =                         None
        self.reply_message_id =                 None
        self.reply_message_text =               None
        self.reply_message_is_text =            None
        self.reply_usr_id =                     None
        self.reply_usr_first =                  None
        self.reply_usr_last =                   None
        self.reply_usr_name =                   None
        self.reply_forward_usr_id =             None
        self.reply_forward_usr_first =          None
        self.reply_is_forward =                 None
        self.caption =                          None
        self.sticker_emoji =                    None
        self.sticker_set_name =                 None
        self.sticker_is_animated =              None
        self.forward_from_id =                  None
        self.is_forwarded =                     None
        self.forward_sender_name =              None

        self.inline_id = None
        self.inline_query = None

        user_first =                            ""
        user_last =                             ""
        reply_user_first =                      ""
        reply_user_last =                       ""


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

                get_updates_result = get_updates_result["result"]

                fed_message = get_updates_result["message"]
                self.update_id = get_updates_result["update_id"]

        
        except:
            try:
                try:
                    #intended
                    inline_query = get_updates_result["inline_query"]

                    #update ID
                    self.update_id = get_updates_result["update_id"]
                    self.type = "inline"

                except:
                    #in case

                    get_updates_result = get_updates_result["result"]

                    inline_query = get_updates_result["inline_query"]
                    self.update_id = get_updates_result["update_id"]
                    self.type = "inline"
            
            except:
                print("ERROR: can't get result")
                self.content = None
                return


        #try to get message content in json
        #doing it one by one with try except
        #starting with the most common file type to the less common one
        #only text, sticker, photo supported
        #there's probably a better solution I don't know
        if self.type != "inline":
            try:
                self.content = fed_message["text"]
                self.type = "text"
            except:
                pass

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


            #name
            user_first = fed_message["from"]["first_name"]
            try: 
                user_last = fed_message['from']['last_name']
                self.usr_last = user_last
                self.usr_name = f"{user_first} {user_last}"
            except:
                self.usr_name = f"{user_first}"

            self.usr_first = user_first

            #message ID
            self.message_id = fed_message["message_id"]

            #userID
            self.usr_id = fed_message["from"]["id"]

            try:
                self.forward_from_id = fed_message["forward_from"]["id"]
                self.is_forwarded = True
                #name
                f_user_first = fed_message["forward_from"]["first_name"]
                try: 
                    f_user_last = fed_message['forward_from']['last_name']
                    self.forward_sender_name = f"{f_user_first} {f_user_last}"
                except:
                    self.forward_sender_name = f"{f_user_first}"

                self.usr_first = user_first
            except:
                try:
                    self.forward_sender_name = fed_message["forward_sender_name"]
                    self.is_forwarded = True
                except:
                    pass
            
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
                reply_user_first = fed_message["reply_to_message"]["from"]["first_name"]
                try:
                    reply_user_last = fed_message['reply_to_message']['from']['last_name']
                    self.reply_usr_last = reply_user_last
                    self.reply_usr_name = f"{reply_user_first} {reply_user_last}"
                except:
                    self.reply_usr_name = f"{reply_user_first}"

                self.reply_usr_first = reply_user_first

                
                try:
                    #check if reply message is forwared
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
            
            # for stickers
            try:
                self.file_unique_id = fed_message["sticker"]["file_unique_id"]
                self.content = fed_message["sticker"]["file_id"]
                self.type = "sticker"
                self.sticker_emoji = fed_message["sticker"]["emoji"]
                self.sticker_is_animated = fed_message["sticker"]["is_animated"]
                try:
                    self.sticker_set_name = fed_message["sticker"]["set_name"]
                except:
                    pass
            except:
                pass


            # for documents


            # photo id will be the largest one(the third one)

            try:
                try:
                    self.content = fed_message["photo"][2]["file_id"]
                except:
                    try:
                        self.content = fed_message["photo"][1]["file_id"]
                    except:
                        self.content = fed_message["photo"][0]["file_id"]

                self.type = "photo"
                try:
                    self.caption = fed_message["caption"]
                except:
                    pass
            except:
                pass


            try:
                self.content = fed_message["document"]["file_id"]
                self.type = "document"
                try:
                    self.caption = fed_message["caption"]
                except:
                    pass
            except:
                pass


            try:
                self.content = fed_message["animation"]["file_id"]
                self.type = "animation"
                try:
                    self.caption = fed_message["caption"]
                except:
                    pass
            except:
                pass


            try:
                self.content = fed_message["audio"]["file_id"]
                self.type = "audio"
                try:
                    self.caption = fed_message["caption"]
                except:
                    pass
            except:
                pass

            try:
                self.content = fed_message["video"]["file_id"]
                self.type = "video"
                try:
                    self.caption = fed_message["caption"]
                except:
                    pass
            except:
                pass
        else:


            # inline queries

            self.inline_id = inline_query["id"]

            user_first = inline_query["from"]["first_name"]
            try: 
                user_last = inline_query['from']['last_name']
                self.usr_last = user_last
                self.usr_name = f"{user_first} {user_last}"
            except:
                self.usr_name = f"{user_first}"

            self.usr_first = user_first

            self.usr_id = inline_query["from"]["id"]
            self.inline_query = inline_query["query"]


class chat():
    def __init__(self, chat_info):
        self.chat_id =                      None
        self.chat_title =                   None
        self.chat_type =                    None
        self.chat_bio =                     None
        self.can_send_messages =            False
        self.can_send_media_messages =      False
        self.can_send_polls =               False
        self.can_send_other_messages =      False
        self.can_add_web_page_previews =    False
        self.can_change_info =              False
        self.can_invite_users =             False
        self.can_pin_messages =             False
        self.chat_photo_id =                None
        self.ok =                           True

        user_first =                        ""
        user_last =                         ""

        if chat_info is None:
            print('chat_organizr: no such chat')
            exit()
        else:
            #chat_info = json.loads(str(chat_info))
            pass
        try:
            try:
                #intended
                self.chat_id = chat_info["id"]

                self.chat_type = chat_info["type"]

                if self.chat_type != "private":
                    try:
                        self.chat_bio = chat_info["description"]
                    except:
                        self.chat_bio = None
                    self.chat_title = chat_info["title"]

                else:
                    try:
                        self.chat_bio = chat_info["bio"]
                    except:
                        self.chat_bio = None
                    self.chat_title = chat_info["first_name"]

                if self.chat_type != "private":
                    chat_permissions = chat_info["permissions"]
                else:
                    pass

                try:
                    self.chat_photo_id = chat_info["photo"]["big_file_id"]
                except:
                    try:
                        self.chat_photo_id = chat_info["photo"]["small_file_id"]
                    except:
                        self.chat_photo_id = None

            except:
                #in case
                self.chat_id = chat_info["result"]["id"]

                self.chat_type = chat_info["result"]["type"]

                if self.chat_type != "private":
                    try:
                        self.chat_bio = chat_info["result"]["description"]
                    except:
                        self.chat_bio = None
                    self.chat_title = chat_info["result"]["title"]

                else:
                    try:
                        self.chat_bio = chat_info["result"]["bio"]
                    except:
                        self.chat_bio = None

                    user_first = chat_info["result"]["first_name"]
                    try:
                        user_last = chat_info['result']['last_name']
                        self.chat_title = f"{user_first} {user_last}"
                    except:
                        self.chat_title = f"{user_first}"

                if self.chat_type != "private":
                    chat_permissions = chat_info["result"]["permissions"]
                else:
                    pass

                try:
                    self.chat_photo_id = chat_info["result"]["photo"]["big_file_id"] 
                except:
                    try:
                        self.chat_photo_id = chat_info["photo"]["small_file_id"]
                    except:
                        self.chat_photo_id = None


        except:
            print("ERROR: can't get chat result")
            self.ok = False
            return

        if self.chat_type != "private":
            if chat_permissions["can_send_messages"] == "true":
                self.can_send_messages = True

            if chat_permissions["can_send_media_messages"] == "true":
                self.can_send_media_messages = True

            if chat_permissions["can_send_polls"] == "true":
                self.can_send_polls = True

            if chat_permissions["can_send_other_messages"] == "true":
                self.can_send_other_messages = True

            if chat_permissions["can_add_web_page_previews"] == "true":
                self.can_add_web_page_previews = True

            if chat_permissions["can_change_info"] == "true":
                self.can_change_info = True

            if chat_permissions["can_invite_users"] == "true":
                self.can_invite_users = True

            if chat_permissions["can_pin_messages"] == "true":
                self.can_pin_messages = True


class bot():
    def __init__(self, bot_info):
        self.id = None
        self.first_name = None
        self.username = None
        self.can_join_groups = None
        self.can_read_all_group_messages = None
        self.supports_inline_queries = None
        self.ok = True

        if bot_info is None:
            print("ERROR: can't get bot info")
            self.ok = False
        else:
            pass

        try:
            self.id = bot_info["id"]
            self.first_name = bot_info["first_name"]
            self.username = bot_info["username"]
            self.can_join_groups = bot_info["can_join_groups"]
            self.can_read_all_group_messages = bot_info["can_read_all_group_messages"]
            self.supports_inline_queries = bot_info["supports_inline_queries"]
        except:
            bot_info = bot_info["result"]
            self.id = bot_info["id"]
            self.first_name = bot_info["first_name"]
            self.username = bot_info["username"]
            self.can_join_groups = bot_info["can_join_groups"]
            self.can_read_all_group_messages = bot_info["can_read_all_group_messages"]
            self.supports_inline_queries = bot_info["supports_inline_queries"]