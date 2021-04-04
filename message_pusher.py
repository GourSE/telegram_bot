# coding=utf-8

from colours import colour
from getpass import getuser
from core import telegram_bot_api
import configparser as cfg
import time
import random
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

alert = False

try:
    is_send_typing = config.get("settings", "send_typing")
except:
    alert = True
    is_send_typing = True
try:
    is_markdown = config.get("settings", "use_markdown")
except:
    alert = True
    is_markdown = False

if alert:
    print(f"{colour.RED}there is a new version of config.cfg, will set some setings to default{colour.reset}")
else:
    pass

# set user settings
if is_send_typing.lower() == "true":
    is_send_typing = True
elif is_send_typing.lower() == "false":
    is_send_typing = False

if is_markdown.lower() == "true":
    is_markdown = True
elif is_markdown.lower() == "false":
    is_markdown = False


def message_type_prompt(last_chat_id=None):
    fed = input("\nMessage types:\ntext(t)\nsticker(s)\nEnter message type > $ ")
    fed = fed.lower()
    if fed == "text" or fed == "t" or fed == "1":
        return "text"
    elif fed == "sticker" or fed == "s" or fed == "2":
        return "sticker"
    elif fed == ":q":
        print(f"{colour.GREEN}abort{colour.reset}\n")
        master(last_chat_id)
    else:
        print("\n{}{} is not a message type{}\n".format(colour.RED, fed, colour.reset))
        time.sleep(0.5)
        return message_type_prompt(last_chat_id)

def sticker_prompt(chat_id):
    success = None
    fed = input("Enter sticker ID > $ ")
    if fed == ":q":
        print(f"{colour.GREEN}abort{colour.reset}\n")
        time.sleep(0.5)
        master(chat_id)
    else:
        try:
            success = bot.send_sticker(chat_id, fed)
            if success:
                print("sticker sent")
            else:
                print("sticker not sent\n")
            sticker_prompt(chat_id)
        except:
            print("Something went wrong\nMake sure the sticker ID is correct\n")
            time.sleep(0.5)
            sticker_prompt(chat_id)

def send_typing(text, chat_id):
    lenght = len(text)
    loop = int(lenght * 0.2)
    while loop > 0:
        loop -= 1
        bot.send_chat_action(chat_id, "typing")

def text_prompt(chat_id):
    success = None
    global is_markdown
    global is_send_typing

    fed = input("Enter text message > $ ")
    if fed == ":q":
        print(f"{colour.GREEN}abort{colour.reset}\n")
        master(chat_id)
    else:
        fedf = textf.hex(fed)

        try:

            if is_send_typing:
                send_typing(fed, chat_id)
                success = bot.send_message(chat_id, fedf, is_markdown=is_markdown)
                if success:
                    print(f"message: \"{fed}\" sent")
                else:
                    print(f"message: \"{fed}\" not send\n")
                text_prompt(chat_id)
            else:
                success = bot.send_message(chat_id, fedf, None, is_markdown)
                if success:
                    print(f"message: \"{fed}\" sent")
                else:
                    print(f"message: \"{fed}\" not send\n")
                text_prompt(chat_id)


        except Exception as ERROR:
            print(f"\nSomething went wrong, more info:\n{ERROR}\n\n")
            time.sleep(0.5)
            text_prompt(chat_id)


def master(last_chat_id=None):
    if last_chat_id is not None:
        fed = input("Use previous chat ID?(Y/n) > $ ")
        fedf = fed[0].lower()
        # print(fed)
        if fedf == "y":
            chat_id = last_chat_id
        elif fedf == "n":
            chat_id = input("Ener chat ID: ")
        elif fed == ":q":
            print(f"{colour.GREEN}quit{colour.reset}\n")
            os._exit(1)
        else:
            print(f"{colour.RED}{fed} is not a valid answer{colour.reset}\nuse (Y/n)\n")
            time.sleep(1)
            master(last_chat_id)
    
    else:
        while True:
            chat_id = input("Ener chat ID > $ ")
            if chat_id == "":
                print(f"{colour.RED}you entered nothing{colour.reset}\n")
                time.sleep(1)
            elif chat_id == ":q":
                print(f"{colour.GREEN}quit{colour.reset}\n")
                os._exit(1)
            else:
                break

    message_type = message_type_prompt(last_chat_id)
    print("You are going to send {} message(s) to chat id: {}".format(message_type, chat_id))
    if message_type == "sticker":
        sticker_prompt(chat_id)
    elif message_type == "text":
        text_prompt(chat_id)
    else:
        print(f"{colour.RED}ERROR: MESSAGE_TYPE_INVALID{colour.reset}")


master()