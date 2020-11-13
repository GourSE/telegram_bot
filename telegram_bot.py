# coding=utf-8

from message_organizer import message as morg
import configparser as cfg
from core import telegram_bot_api
import threading
import time

# This is a testing script to combine support_bot.py and message_pusher.py


bot = telegram_bot_api("config.cfg")

config = cfg.ConfigParser()
config.read("config.cfg")
admin_id = config.get("settings", "admin_id")
is_send_typing = config.get("settings", "send_typing")
is_markdown = config.get("settings", "use_markdown")

# set user settings 
# get lowers from true and false

if is_send_typing.lower() == "true":
    is_send_typing = True
elif is_send_typing.lower() == "false":
    is_send_typing = False

if is_markdown.lower() == "true":
    is_markdown = True
elif is_markdown.lower() == "false":
    is_markdown = False

# functions for bot support

# notufy admin with forwarded message from user who sent message to the bot
# the admin "will" know who sent the message except for those who disabled the feature

def notify_admin(is_group, from_chat_id, message_id):
    global admin_id

    if is_group:
        return
    else:
        pass

    bot.forward_message(admin_id, from_chat_id, message_id)

    return

# reply to user with reguler messages and stickers
# will probably add photos support
# the bot will not forward message from admin, so your account will not be shown

def reply_to_usr(message_content, reply_usr_id, message_type):
    if message_type == "text":
        bot.send_message(reply_usr_id, message_content)
    elif message_type == "sticker":
        sticker_id = message_content.replace("sticker: ", "")
        bot.send_sticker(reply_usr_id, sticker_id)

def message_pusher(message_content, chat_id, message_type):
    if message_type == "text":
        bot.send_message(chat_id, message_content)
    elif message_type == "sticker":
        sticker_id = message_content.replace("sticker: ", "")
        bot.send_sticker(chat_id, sticker_id)

# master of support bot

def supprot_master():
    global admin_id

    print("start updating messages real-time\n")
    offset = None
    while True:
        update = bot.get_updates(offset)
        try:
            for item in update["result"]:
                msg = morg(item)
                bash_output = f"message sent by {msg.usr_first}, content: {msg.content}\n"
                offset = msg.update_id
                # this will let the bot to skip the messages from admins forwarding back into the admin chat
                if str(msg.chat_id) != str(admin_id):
                    print(bash_output)
                    if msg.is_group:
                        pass
                    else:
                        try:
                            notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id))
                            notify_thread.start()
                        
                        except RuntimeError as error:
                            print(f"ERROR: message postponed\nRuntimeError: {error}")
                            time.sleep(3)
                            notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id))
                            notify_thread.start()
                            print("thread started")
                        
                        except Exception as error:
                            print(f"ERROR: unknown error, the script will stop\n{error}")
                            exit()
                elif msg.reply_is_forward:
                    bash_output = f"admin replied to {msg.reply_forward_usr_first}, content: {msg.content}\n"
                    print(bash_output)
                    try:
                        reply_thread = threading.Thread(target=reply_to_usr, args=(msg.content, msg.reply_usr_id, msg.type))
                        reply_thread.start()

                    except RuntimeError as error:
                        print(f"ERROR: message postponed\nRuntimeError: {error}")
                        reply_thread = threading.Thread(target=reply_to_usr, args=(msg.content, msg.reply_usr_id, msg.type))
                        reply_thread.start()
                        print("thread started")

                    except Exception as error:
                        print(f"ERROR: unknown error, the script will stop\n{error}")
                        exit()
                elif msg.reply_message_is_text:
                    bash_output = f"admin sent a message to chat ID: {msg.reply_message_text}, content: {msg.content}\n "
                    print(bash_output)
                    try:
                        send_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_message_text, msg.type))
                        send_thread.start()

                    except RuntimeError as error:
                        print(f"ERROR: message postponed\nRuntimeError: {error}")
                        send_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_message_text, msg.type))
                        send_thread.start()
                        print("thread started")

        except KeyError as error:
            print(f"ERROR: no bot token or another getUpdate session running\nplese check 'config.cfg'\n\nKeyError: {error}\n")

        except RuntimeError as error:
            print(f"ERROR: RuntimeError: {error}\nwill continue looping")
            time.sleep(3)

        except Exception as error:
            print(f"ERROR: unknown error, the script will stop\n{error}")
            exit()


supprot_master()