# coding=utf-8

from message_organizer import message as morg
import configparser as cfg
from core import telegram_bot_api
import threading
import time


bot = telegram_bot_api("config.cfg")

config = cfg.ConfigParser()
config.read("config.cfg")
admin_id = config.get("support", "admin_id")

def notify_admin(is_group, from_chat_id, message_id):
    global admin_id

    if is_group:
        return
    else:
        pass

    bot.forward_message(admin_id, from_chat_id, message_id)
    return

def reply_to_usr(message_content, reply_usr_id, message_type):
    if message_type == "text":
        bot.send_message(reply_usr_id, message_content)
    elif message_type == "sticker":
        sticker_id = message_content.replace("sticker: ", "")
        bot.send_sticker(reply_usr_id, sticker_id)

def master():
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
                    bash_output = f"admin replied to {msg.reply_forward_usr_first}, content: {msg.content}"
                    print(bash_output)
                    try:
                        send_thread = threading.Thread(target=reply_to_usr, args=(msg.content, msg.reply_forward_usr_id, msg.type))
                        send_thread.start()

                    except RuntimeError as error:
                        print(f"ERROR: message postponed\nRuntimeError: {error}")
                        send_thread = threading.Thread(target=reply_to_usr, args=(msg.content, msg.reply_forward_usr_id, msg.type))
                        send_thread.start()
                        print("thread started")

                    except Exception as error:
                        print(f"ERROR: unknown error, the script will stop\n{error}")
                        exit()

        except KeyError as error:
            print(f"ERROR: no bot token or another getUpdate session running\nplese check 'config.cfg'\n\nKeyError: {error}\n")

        except RuntimeError as error:
            print(f"ERROR: RuntimeError: {error}\nwill continue looping")
            time.sleep(3)

        except Exception as error:
            print(f"ERROR: unknown error, the script will stop\n{error}")
            exit()


master()