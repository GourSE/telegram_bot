# coding=utf-8

from colours import colour
from getpass import getuser
from core import telegram_bot_api
import configparser as cfg
import time
import random
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

is_send_typing = config.get("settings", "send_typing")
is_markdown = config.get("settings", "use_markdown")

# set user settings
if is_send_typing.lower() == "true":
    is_send_typing = True
elif is_send_typing.lower() == "false":
    is_send_typing = False

if is_markdown.lower() == "true":
    is_markdown = True
elif is_markdown.lower() == "false":
    is_markdown = False


# def chat_id_prompt():
#     fed = input("Ener chat ID: ")

#     the chat ID could be user's ID

#     if fed.__len__() < 9:
#         print("Are you sure this is a chat id?\n")
#         time.sleep(0.5)
#         return chat_id_prompt()
#     else:
#         return fed

#     return fed

def message_type_prompt():
    fed = input("\nMessage types:\ntext(t)\nsticker(s)\nEnter message type: ")
    fed = fed.lower()
    if fed == "text" or fed == "t":
        return "text"
    elif fed == "sticker" or fed == "s":
        return "sticker"
    else:
        print("\n{}{} is not a message type{}\n".format(colour.RED, fed, colour.reset))
        time.sleep(0.5)
        return message_type_prompt()

def sticker_prompt(chat_id):
    success = None
    fed = input("Enter sticker ID: ")
    if fed == ":q":
        print("abord\n")
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

def text_prompt(chat_id, is_markdown):
    success = None
    
    # if is_markdown == None:
    #     is_markdown = input("Do you want to use MarkdownV2 in this message?\n(Y/n): ")
    #     is_markdown = is_markdown[0].lower()
    #     if is_markdown == "y":
    #         is_markdown = True
    #     elif is_markdown == "n":
    #         is_markdown = False
    #     elif is_markdown == ":q":
    #         print("abord\n")
    #         time.sleep(0.5)
    #         master(chat_id)
    #     else:
    #         print("Plese enter 'y' for yes and 'n' for no")
    #         text_prompt(chat_id, is_markdown)

    fed = input("Enter text message: ")
    if fed == ":q":
        print("abord\n")
        time.sleep(0.5)
        master(chat_id)
    else:
        try:

            if is_send_typing:
                send_typing(fed, chat_id)
                success = bot.send_message(chat_id, fed, None, is_markdown)
                if success:
                    print(f"message: \"{fed}\" sent")
                else:
                    print(f"message: \"{fed}\" not send\n")
                text_prompt(chat_id, is_markdown)
            else:
                success = bot.send_message(chat_id, fed, None, is_markdown)
                if success:
                    print(f"message: \"{fed}\" sent")
                else:
                    print(f"message: \"{fed}\" not send\n")
                text_prompt(chat_id, is_markdown)


        except Exception as ERROR:
            print(f"\nSomething went wrong, more info:\n{ERROR}\n\n")
            time.sleep(0.5)
            text_prompt(chat_id, None)


def master(last_chat_id):
    if last_chat_id is not None:
        fed = input("Do you want to use your last chat ID?\n(Y/n): ")
        fed = fed[0].lower()
        print(fed)
        if fed == "y":
            chat_id = last_chat_id
        else:
            chat_id = input("Ener chat ID: ")
    else:
        chat_id = input("Ener chat ID: ")

    message_type = message_type_prompt()
    print("You are going to send {} message(s) to chat id: {}".format(message_type, chat_id))
    if message_type == "sticker":
        sticker_prompt(chat_id)
    elif message_type == "text":
        text_prompt(chat_id, None)
    else:
        print(f"{colour.RED}ERROR: MESSAGE_TYPE_INVALID{colour.reset}")


master(None)