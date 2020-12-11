# coding=utf-8

from colours import colour
from message_organizer import message as morg
import configparser as cfg
from core import telegram_bot_api
import threading
import time



bot = telegram_bot_api("config.cfg")

config = cfg.ConfigParser()
config.read("config.cfg")
admin_id = config.get("settings", "admin_id")
is_send_typing = config.get("settings", "send_typing")
is_markdown = config.get("settings", "use_markdown")

if admin_id == "admin chat ID here":
    
    admin_id = input(f"\
\n{colour.RED}You did not enter an admin chat ID{colour.reset}\n\
An admin chat ID can be both a group or a user chat ID\n\
The chat ID you enter now will not be saved\n\
Enter admin chat ID: ")

else:
    pass

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


# admin "will" know who sent the message

def notify_admin(is_group, from_chat_id, message_id, usr_first):
    global admin_id

    if is_group:
        return
    else:
        pass

    s = bot.send_message_markdown(admin_id, f"[{usr_first}](tg://user?id={from_chat_id})")
    
    if s:
        pass
    else:
    
        print(f"{colour.RED}cannot send user info to admin{colour.reset}\n{colour.red}user first name: {usr_first}, user ID: {from_chat_id}{colour.reset}\n\n")
    s = bot.forward_message(admin_id, from_chat_id, message_id)

    if s:
        pass
    else:
        print(f"{colour.RED} unable to forward message to admin{colour.reset}\n{colour.red}user first name: {usr_first}, user ID: {from_chat_id}{colour.reset}\n\n")

    return

# reply to user with reguler messages and stickers
# will probably add photos support
# the bot will not forward message from admin, so your account will not be shown

def message_pusher(message_content, chat_id, message_type):
    if message_type == "text":
        s = bot.send_message(chat_id, message_content)
        if s:
            print(f"{colour.green}admin replied to chat ID: {chat_id}{colour.reset}, content: {colour.yellow}{message_content}{colour.reset}\n")
        else:
            print(f"admin replying to chat ID: {chat_id} {colour.RED}is not successful{colour.reset}, \ncontent: {colour.yellow}{message_content}{colour.reset}\n")
    elif message_type == "sticker":
        sticker_id = message_content.replace("sticker: ", "")
        s = bot.send_sticker(chat_id, sticker_id)
        if s:
            print(f"{colour.green}admin replied to {chat_id}{colour.reset}, {colour.yellow}{message_content}{colour.reset}\n")
        else:
            print(f"admin replying to {chat_id} {colour.RED}is not successful{colour.reset}, \n{colour.yellow}{message_content}{colour.reset}\n")


def master():
    global admin_id

    print("start updating messages real-time\n")
    offset = None
    while True:
        update = bot.get_updates(offset)
        try:
            for item in update["result"]:
                msg = morg(item)
                bash_output = f"{colour.green}message sent by {msg.usr_first}{colour.reset}, content: {colour.yellow}{msg.content}{colour.reset}\n"
                offset = msg.update_id
                # this will let the bot to skip the messages from admins forwarding back into the admin chat
                if str(msg.chat_id) != str(admin_id):
                    print(bash_output)
                    if msg.is_group:
                        pass
                    else:
                        try:
                            notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id, msg.usr_first))
                            notify_thread.start()
                        
                        except RuntimeError as error:
                            print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                            time.sleep(3)
                            notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id, msg.usr_first))
                            notify_thread.start()
                            print("thread started")
                        
                        except Exception as error:
                            print(f"{colour.WARNING}ERROR: unknown error{colour.reset}, the script will stop\n{error}")
                            exit()
                elif msg.reply_is_forward:
                    bash_output = f"admin replied to {msg.reply_forward_usr_first}, content: {msg.content}\n"
                    # print(bash_output)
                    try:
                        reply_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_forward_usr_id, msg.type))
                        reply_thread.start()

                    except RuntimeError as error:
                        print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                        reply_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_forward_usr_id, msg.type))
                        reply_thread.start()
                        print("thread started")

                    except Exception as error:
                        print(f"{colour.WARNING}ERROR: unknown error{colour.reset}, the script will stop\n{error}")
                        exit()
                elif msg.reply_message_is_text:
                    bash_output = f"admin sent a message to chat ID: {msg.reply_message_text}, content: {msg.content}\n "
                    # print(bash_output)
                    try:
                        send_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_message_text, msg.type))
                        send_thread.start()

                    except RuntimeError as error:
                        print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                        send_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_message_text, msg.type))
                        send_thread.start()
                        print("thread started")

        except KeyError as error:
            print(f"{colour.WARNING}ERROR: no bot token{colour.RED} or another getUpdate session running{colour.reset}\n{colour.YELLOW}plese check 'config.cfg'\n\nKeyError: {error}{colour.reset}\n")
            exit()

        except RuntimeError as error:
            print(f"{colour.RED}ERROR: RuntimeError: {error}{colour.reset}\nwill continue looping")
            time.sleep(3)

        except Exception as error:
            print(f"{colour.WARNING}ERROR: unknown error, the script will stop{colour.reset}\n{error}")
            exit()


master()