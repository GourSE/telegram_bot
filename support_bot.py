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
import textf

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

def notify_admin(is_group, from_chat_id, message_id):
    global admin_id

    if is_group:
        return
    else:
        pass

    s = bot.forward_message(admin_id, from_chat_id, message_id)
    if s:
        pass
    else:
        print(f"forwarding message: {colour.BOLD}{message_id}{colour.reset} to admin is {colour.RED}unsuccessful{colour.reset}\n{colour.YELLOW}please check if the admin chat ID is correct{colour.reset}\n ")

    return

def reply_to_usr(message_content, reply_usr_id, message_type, caption):
    caption = textf.hex(caption)
    if message_type == "text":
        s = bot.send_message(reply_usr_id, textf.hex(message_content), None, False)
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
        s = bot.send_photo(reply_usr_id, photo_id=message_content, text=caption)
        if s:
            print(f"{colour.BOLD}photo{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}photo{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "document":
        s = bot.send_document(reply_usr_id, document_id=message_content, text=caption)
        if s:
            print(f"{colour.BOLD}document{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}document{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "animation":
        s = bot.send_animation(reply_usr_id, animation_id=message_content, text=caption)
        if s:
            print(f"{colour.BOLD}animation{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}animation{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "audio":
        s = bot.send_audio(reply_usr_id, audio_id=message_content, text=caption)
        if s:
            print(f"{colour.BOLD}audio{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}audio{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "video":
        s = bot.send_video(reply_usr_id, video_id=message_content, text=caption)
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
                            print(f"ERROR: RuntimeError, message postponed")
                            time.sleep(3)
                            notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id))
                            notify_thread.start()
                            print("thread started")
                        
                        except Exception as error:
                            print(f"\nERROR: unknown error, the script will end\n\n{error}")
                            exit()
                elif msg.reply_is_forward:
                    bash_output = f"admin replied to {msg.reply_forward_usr_first}, content: {msg.content}"
                    #print(bash_output)
                    try:
                        send_thread = threading.Thread(target=reply_to_usr, args=(msg.content, msg.reply_forward_usr_id, msg.type, msg.caption))
                        send_thread.start()

                    except RuntimeError as error:
                        print(f"\nERROR: message postponed\nRuntimeError: \n\n{error}\n\n")
                        send_thread = threading.Thread(target=reply_to_usr, args=(msg.content, msg.reply_forward_usr_id, msg.type, msg.caption))
                        send_thread.start()
                        print("thread started")

                    except Exception as error:
                        print(f"\nERROR: unknown error, the script will end\n\n{error}")
                        exit()

        except KeyError as error:
            print(f"\nERROR: no bot token or another getUpdate session running\nplese check 'config.cfg'\n\nKeyError: \n\n{error}\n\n")

        except RuntimeError as error:
            print(f"\nERROR: RuntimeError: \n\n{error}\n\nwill continue looping\n\n")
            time.sleep(3)

        except Exception as error:
            print(f"\nERROR: unknown error, the script will stop\n\n{error}\n\n")
            exit()


master()