# coding=utf-8

from colours import colour
from getpass import getuser
from organizer import message as morg
from organizer import chat as corg
import configparser as cfg
from core import telegram_bot_api
import threading
import time
import platform
import os
import textf
import start_ignore


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
    admin_id = config.get("settings", "admin_id")
except:
    admin_id = 0
    alert = True
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
try:
    default_chat = config.get("settings", "default_chat")
except:
    alert = True
    default_chat = 0
try:
    default_chat_echo = config.get("settings", "echo")
except:
    alert = True
    default_chat_echo = False
try:
    is_start_ignore = config.get("settings", "ignore_old_message")
except:
    alert = True
    is_start_ignore = True

default_chat_echo_mention = False

if alert:
    print(f"{colour.RED}there is a new version of config.cfg, will set some setings to default{colour.reset}")
else:
    pass

# empty deafult chat will be 0
if default_chat == "deafult chat here" or default_chat == 0:
    default_chat = 0

if admin_id == "admin chat ID here" or admin_id == 0:
    
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

if default_chat_echo.lower() == "true":
    default_chat_echo_mention = True
    default_chat_echo = True
elif default_chat_echo.lower() == "false":
    default_chat_echo_mention = False
    default_chat_echo = False
elif default_chat_echo.lower() == "mention":
    default_chat_echo = False
    default_chat_echo_mention = True

if is_start_ignore.lower() == "true":
    is_start_ignore = True
elif is_start_ignore.lower() == "false":
    is_start_ignore = False


def send_typing(text, chat_id):
    lenght = len(text)
    loop = int(lenght * 0.2)
    while loop > 0:
        loop -= 1
        bot.send_chat_action(chat_id, "typing")

# admin "will" know who sent the message

def notify_admin(is_group, from_chat_id, message_id, usr_first, mention=None, usr_id=""):
    global admin_id
    global is_markdown

    if mention:
        s = bot.forward_message(admin_id, from_chat_id, message_id)
        if is_markdown:
            a = bot.send_message(admin_id, f"[{textf.hex(textf.escape(usr_first))}](tg://user?id={textf.hex(str(usr_id))})")
        else:
            a = True
        if s and a:
            return
        else:
            print(f"{colour.RED}echo from {chat_id}  error{colour.reset}")
        return
    elif mention is False:
        s = bot.forward_message(admin_id, from_chat_id, message_id)
        if s:
            return
        else:
            print(f"{colour.RED}echo from {chat_id}  error{colour.reset}")
        return
    else:
        pass


    if is_group:
        return
    else:
        pass

    s = bot.forward_message(admin_id, from_chat_id, message_id)

    if s:
        pass
    else:
        print(f"{colour.RED} unable to forward message to admin{colour.reset}\n{colour.red}user first name: {usr_first}, user ID: {from_chat_id}{colour.reset}\n\n")

    s = bot.send_message(admin_id, f"[{textf.hex(usr_first)}](tg://user?id={textf.escape(str(from_chat_id))})", None, True)
    
    if s:
        pass
    else:
        print(f"{colour.RED}cannot send user info to admin{colour.reset}\n{colour.red}user first name: {usr_first}, user ID: {from_chat_id}{colour.reset}\n\n")
    
    return

# reply to user with reguler messages and stickers
# will probably add photos support
# the bot will not forward message from admin, so your account will not be shown

def message_pusher(message_content, chat_id, message_type, caption=None):
    global is_markdown
    global is_send_typing
    global default_chat_echo

    caption = textf.hex(caption)

    if message_type == "text":
        if is_send_typing:
            send_typing(message_content, chat_id)

        message_content = textf.hex(message_content)

        s = bot.send_message(chat_id, message_content, is_markdown=is_markdown)
        if s:
            print(f"admin replied to {chat_id}, content: {colour.BOLD}{message_content}{colour.reset}\n")
        else:
            print(f"message: {colour.BOLD}{message_content}{colour.reset} for {chat_id} {colour.RED}not sent{colour.reset}\n ")
    elif message_type == "sticker":
        sticker_id = message_content.replace("sticker: ", "")
        s = bot.send_sticker(chat_id, sticker_id)
        if s:
            print(f"{colour.BOLD}sticker{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}sticker{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "photo":
        s = bot.send_photo(chat_id, photo_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}photo{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}photo{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "document":
        s = bot.send_document(chat_id, document_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}document{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}document{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "animation":
        s = bot.send_animation(chat_id, animation_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}animation{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}animation{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "audio":
        s = bot.send_audio(chat_id, audio_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}audio{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}audio{colour.reset} {colour.RED}not sent{colour.reset}\n")

    elif message_type == "video":
        s = bot.send_video(chat_id, video_id=message_content, text=caption, is_markdown=is_markdown)
        if s:
            print(f"{colour.BOLD}video{colour.reset} sent\n")
        else:
            print(f"{colour.BOLD}video{colour.reset} {colour.RED}not sent{colour.reset}\n")

def admin_message_handler(msg, msg_type, reply_message_id, reply_message_text, reply_is_text, caption=None):
    # because reply_is_text is only True when it's actually a reply_to
    # so I'll have to check for this one time only
    
    global default_chat
    global is_markdown
    global default_chat_echo
    global default_chat_echo_mention

    if "/id " in msg or msg == "/id":
        msg = msg.replace("/id ", "")
        default_chat = msg
        message_pusher("Done", admin_id, "text")
        return
    elif "/md " in msg or msg == "/md":
        msg = msg.replace("/md ", "")
        if msg == "True" or msg == "true" or msg == "yes" or msg == "1":
            is_markdown = True
            message_pusher("markdown is now True", admin_id, "text")
            return
        elif msg == "False" or msg == "false" or msg == "no" or msg == "0":
            is_markdown = False
            message_pusher("markdown is now False", admin_id, "text")
            return
        else:
            if is_markdown:
                is_markdown = False
                message_pusher("markdown is now False", admin_id, "text")
            elif not is_markdown:
                is_markdown = True
                message_pusher("markdown is now True", admin_id, "text")
            else:
                is_markdown = True
                message_pusher("markdown is now True", admin_id, "text")
    elif "/echo " in msg or msg == "/echo":
        msg = msg.replace("/echo ", "")
        if msg == "True" or msg == "true" or msg == "yes" or msg == "1":
            default_chat_echo_mention = True
            default_chat_echo = True
            message_pusher("echo is now True", admin_id, "text")
            return
        elif msg == "False" or msg == "false" or msg == "no" or msg == "0":
            default_chat_echo_mention = False
            default_chat_echo = False
            message_pusher("echo is now False", admin_id, "text")
            return
        elif msg == "2" or msg == "mention" or msg == "m":
            default_chat_echo = False
            default_chat_echo_mention = True
            message_pusher("echo is now mention only", admin_id, "text")
            return
        else:
            if default_chat_echo:
                default_chat_echo_mention = False
                default_chat_echo = False
                message_pusher("echo is now False", admin_id, "text")
            elif not default_chat_echo:
                default_chat_echo_mention = True
                default_chat_echo = True
                message_pusher("echo is now True", admin_id, "text")
            else:
                default_chat_echo_mention = True
                default_chat_echo = True
                message_pusher("echo is now True", admin_id, "text")
        return
    elif msg == "/status":
        if default_chat != 0:
            chati = corg(bot.get_chat(default_chat))
            if default_chat_echo_mention and default_chat_echo:
                echo_mode = "True"
            elif default_chat_echo_mention:
                echo_mode = "Mention only"
            else:
                echo_mode = "False"
            bot.send_message(admin_id, f"default chat info\n\nchat title: `{textf.hex(textf.escape(chati.chat_title))}`\nchat ID: `{textf.hex(textf.escape(default_chat))}`\nmarkdown: {is_markdown}\necho: {echo_mode}", is_markdown=True)
        else:
            message_pusher("No chat set", admin_id, "text")
        return
    elif msg == "/reset":
        default_chat = 0
        message_pusher("Done", admin_id, "text")
        return

    elif default_chat != 0:
        message_pusher(msg, default_chat, msg_type, caption=caption)
        return
    else:
        print(f"{colour.RED}ignored an admin message{colour.reset}\n")
        return

def master():
    global admin_id
    global default_chat
    global default_chat_echo

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
                if msg.content is not None:
                    if str(msg.chat_id) == str(admin_id) and msg.reply_message_is_text is not True:
                        try:
                            admin_thread = threading.Thread(target=admin_message_handler, args=(msg.content, msg.type, msg.reply_message_id, msg.reply_message_text, msg.reply_message_is_text, msg.caption))
                            admin_thread.start()
                        
                        except RuntimeError as error:
                            print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                            time.sleep(3)
                            admin_thread = threading.Thread(target=admin_message_handler, args=(msg.msg.content, msg.type, msg.reply_message_id, msg.reply_message_text, msg.reply_message_is_text, msg.caption))
                            admin_thread.start()
                            print("thread started")
                        
                        except Exception as error:
                            print(f"{colour.WARNING}ERROR: unknown error{colour.reset}, the script will stop\n{error}")
                            exit()
                    elif str(msg.chat_id) == str(default_chat):
                        if default_chat_echo and default_chat_echo_mention:
                            try:
                                notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id, msg.usr_first, True, msg.usr_id))
                                notify_thread.start()
                            
                            except RuntimeError as error:
                                print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                                time.sleep(3)
                                notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id, msg.usr_first, True, msg.usr_id))
                                notify_thread.start()
                                print("thread started")
                            
                            except Exception as error:
                                print(f"{colour.WARNING}ERROR: unknown error{colour.reset}, the script will stop\n{error}")
                                exit()
                        elif default_chat_echo:
                            try:
                                notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id, msg.usr_first, False))
                                notify_thread.start()
                            
                            except RuntimeError as error:
                                print(f"{colour.RED}ERROR: message postponed{colour.reset}\nRuntimeError: {error}")
                                time.sleep(3)
                                notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id, msg.usr_first, False))
                                notify_thread.start()
                                print("thread started")
                            
                            except Exception as error:
                                print(f"{colour.WARNING}ERROR: unknown error{colour.reset}, the script will stop\n{error}")
                                exit()
                        else:
                            pass

                    elif str(msg.chat_id) != str(admin_id) and str(default_chat) == "0":
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
                else:
                    pass

        except KeyError as error:
            print(f"{colour.WARNING}ERROR: no bot token{colour.RED} or another getUpdate session running{colour.reset}\n{colour.YELLOW}plese check 'config.cfg'\n\nKeyError: {error}{colour.reset}\n")
            exit()

        except RuntimeError as error:
            print(f"{colour.RED}ERROR: RuntimeError: {error}{colour.reset}\nwill continue looping")
            time.sleep(3)

        except Exception as error:
            print(f"{colour.WARNING}ERROR: unknown error, the script will stop{colour.reset}\n{error}")
            exit()


if is_start_ignore:
    start_ignore.main()
else:
    print(f"{colour.GREEN}ignore old message is set to off{colour.reset}")

master()