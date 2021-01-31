# coding=utf-8

from colours import colour
from getpass import getuser
from organizer import message as morg
import configparser as cfg
from core import telegram_bot_api
import threading
import time
import platform
import os

detected_OS = platform.system()

prgm_path = ""
if detected_OS == "Windows":
    if os.environ.get("PROGRAMFILES(X86)") is None:
        prgm_path = os.environ.get("PROGRAMFILES")
    else:
        prgm_path = os.environ.get("PROGRAMFILES(X86)")

config_path = ["config.cfg", f"/home/{getuser()}/.local/share/telegram_bot/config.cfg", f"{prgm_path}\\GourSE\\telegram_bot\\"]

# Get config file for settings
config = cfg.ConfigParser()
if detected_OS == "Windows":
    try:
        bot = telegram_bot_api(config_path[0])
        config.read(config_path[0])
    except:
        bot = telegram_bot_api(config_path[2])
        config.read(config_path[2])
else:
    try:
        bot = telegram_bot_api(config_path[0])
        config.read(config_path[0])
    except:
        bot = telegram_bot_api(config_path[1])
        config.read(config_path[1])

admin_id = config.get("settings", "admin_id")
is_send_typing = config.get("settings", "send_typing")
is_markdown = config.get("settings", "use_markdown")

if admin_id == "admin chat ID here":
    
    admin_id = input(f"\
\n{colour.RED}You did not enter an admin chat ID{colour.reset}\n\
An admin chat ID can be both a group or a user chat ID\n\
The chat ID you enter now will not be saved\n\
Enter admin chat ID > $ ")
    if admin_id == ":q":
        print(f"{colour.GREEN}quit\n{colour.reset}")
        os._exit(1)
    else:
        pass

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


def send_typing(text, chat_id):
    lenght = len(text)
    loop = int(lenght * 0.2)
    while loop > 0:
        loop -= 1
        bot.send_chat_action(chat_id, "typing")

# admin "will" know who sent the message

def notify_admin(is_group, from_chat_id, message_id, usr_first):
    global admin_id

    if is_group:
        return
    else:
        pass

    s = bot.send_message(admin_id, f"[{usr_first}](tg://user?id={from_chat_id})", None, True)
    
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

def message_pusher(message_content, reply_usr_id, message_type, caption):
    global is_markdown
    global is_send_typing

    if message_type == "text":
        if is_send_typing:
            send_typing(message_content, reply_usr_id)
        s = bot.send_message(reply_usr_id, message_content, is_markdown=is_markdown)
        if s:
            print(f"admin replied to {reply_usr_id}, content: {colour.BOLD}{message_content}{colour.reset}\n")
        else:
            print(f"message: {colour.BOLD}{message_content}{colour.reset} for {reply_usr_id} {colour.RED}not sent{colour.reset}\n ")
    elif message_type == "sticker":
        sticker_id = message_content.replace("sticker: ", "")
        s = bot.send_sticker(reply_usr_id, sticker_id)
        if s:
            print(f"{colour.BOLD}sticker{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}sticker{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "photo":
        s = bot.send_photo(reply_usr_id, photo_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}photo{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}photo{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "document":
        s = bot.send_document(reply_usr_id, document_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}document{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}document{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "animation":
        s = bot.send_animation(reply_usr_id, animation_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}animation{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}animation{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "audio":
        s = bot.send_audio(reply_usr_id, audio_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}audio{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}audio{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "video":
        s = bot.send_video(reply_usr_id, video_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}video{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}video{colour.reset} {colour.RED}not sent{colour.reset}\n")


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
                        reply_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_forward_usr_id, msg.type, msg.caption))
                        reply_thread.start()

                    except RuntimeError as error:
                        print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                        reply_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_forward_usr_id, msg.type, msg.caption))
                        reply_thread.start()
                        print("thread started")

                    except Exception as error:
                        print(f"{colour.WARNING}ERROR: unknown error{colour.reset}, the script will stop\n{error}")
                        exit()
                elif msg.reply_message_is_text:
                    bash_output = f"admin sent a message to chat ID: {msg.reply_message_text}, content: {msg.content}\n "
                    # print(bash_output)
                    try:
                        send_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_message_text, msg.type, msg.caption))
                        send_thread.start()

                    except RuntimeError as error:
                        print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                        send_thread = threading.Thread(target=message_pusher, args=(msg.content, msg.reply_message_text, msg.type, msg.caption))
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