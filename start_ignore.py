from core import telegram_bot_api
import json
import os
from getpass import getuser
from organizer import message as morg
from colours import colour
import platform
import configparser as cfg

def main():
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

    chats = []
    chat_titles = []
    message_count = 0
    offset = None

    while True:
        update = bot.get_updates(offset)
        offset_count = 0

        try:
            for i in update["result"]:
                offset_count += 1
                msg = morg(i)
                try:
                    offset = msg.update_id
                except:
                    break
                if msg.content is not None:
                    message_count += 1
                    if msg.content[0] == '/' or msg.content[0] == "!":
                        print(f"ignored a {colour.GREEN}command{colour.reset} from chat: {colour.CYAN}{msg.chat_title}{colour.reset}")
                        if str(msg.chat_id) not in chats:
                            chats.append(str(msg.chat_id))
                            #chat_titles.append(msg.chat_title)
                        else:
                            pass
                        if str(msg.chat_title) not in chat_titles:
                            chat_titles.append(msg.chat_title)
                        else:
                            pass
                    else:
                        print(f"ignored a {colour.YELLOW}message{colour.reset} from chat: {colour.CYAN}{msg.chat_title}{colour.reset}")
                        if msg.chat_title not in chat_titles:
                            chat_titles.append(msg.chat_title)
                        else:
                            pass
        except Exception as error:
            print(f"unexcpted error: {error} ")
            try:
                offset = msg.update_id
                offset_count += 1
                continue
            except Exception as error:
                print(f"While handling an error, another problen occors\n {error}")
                os._exit(1)
        if offset_count >= 90:
            continue
        else:
            for i in chats:
                # bot.send_message(i, "rebooted", None, False)
                pass
            break
    if message_count != 0:
        print(f"ignored {message_count} messages/commands, from {len(chat_titles)} chats, chats are:")
        for i in chat_titles:
            print(i)
        bot.get_updates(offset)
        print("")
    elif offset_count != 0:
        bot.get_updates(offset)
    else:
        pass
    return message_count