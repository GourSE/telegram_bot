from message_organizer import message as morg
import configparser as cfg
from core import telegram_bot_api
import threading

#This is currently unusebale
#You can only read recived messages 

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

def reply_to_usr(message_content, reply_usr_id):
    bot.send_message(reply_usr_id, message_content)

def master():
    global admin_id

    print("start updating messages real-time")
    offset = None
    while True:
        update = bot.get_updates(offset)
        for item in update["result"]:
            msg = morg(item)
            bash_output = f"message sent by {msg.usr_first}, content: {msg.content}"
            offset = msg.update_id
            if str(msg.usr_id) != str(admin_id):
                print(bash_output)
                if msg.is_group:
                    pass
                else:
                    notify_thread = threading.Thread(target=notify_admin, args=(msg.is_group, msg.usr_id, msg.message_id))
                    notify_thread.start()
            elif msg.reply_is_forward:
                bash_output = f"admin reply to {msg.reply_forward_usr_first}, content: {msg.content}"
                print(bash_output)
                send_thread = threading.Thread(target=reply_to_usr, args=(msg.content, msg.reply_forward_usr_id))
                send_thread.start()


master()