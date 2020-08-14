from core import telegram_bot_api
import time

bot = telegram_bot_api('config.cfg')


def chat_id_prompt():
    fed = input("Ener chat ID: ")
    if fed.__len__() < 9:
        print("Are you sure this is a chat id?\n")
        time.sleep(0.5)
        return chat_id_prompt()
    else:
        return fed

def message_type_prompt():
    fed = input("\nMessage types:\ntext(t)\nsticker(s)\nEnter message type: ")
    fed = fed.lower()
    if fed == "text" or fed == "t":
        return "text"
    elif fed == "sticker" or fed == "s":
        return "sticker"
    else:
        print("{} is not a message type\n".format(fed))
        time.sleep(0.5)
        return message_type_prompt()

def sticker_prompt(chat_id):
    fed = input("Enter sticker ID: ")
    if fed == ":q":
        print("abord\n")
        time.sleep(0.5)
        master(chat_id)
    else:
        try:
            bot.send_sticker(chat_id, fed)
            sticker_prompt(chat_id)
        except:
            print("Something went wrong\nMake sure the sticker ID is correct\n")
            time.sleep(0.5)
            sticker_prompt(chat_id)

def text_prompt(chat_id, is_markdown):
    if is_markdown == None:
        is_markdown = input("Do you want to use MarkdownV2 in this message?\n(Y/n): ")
        is_markdown = is_markdown[0].lower()
        if is_markdown == "y":
            is_markdown = True
        elif is_markdown == "n":
            is_markdown = False
        elif is_markdown == ":q":
            print("abord\n")
            time.sleep(0.5)
            master(chat_id)
        else:
            print("Plese enter 'y' for yes and 'n' for no")
            text_prompt(chat_id, is_markdown)

    fed = input("Enter text message: ")
    if fed == ":q":
        print("abord\n")
        time.sleep(0.5)
        master(chat_id)
    else:
        try:
            if is_markdown == True:
                bot.send_message_markdown(chat_id, fed)
                text_prompt(chat_id, is_markdown)
            else:
                bot.send_message(chat_id, fed)
                text_prompt(chat_id, is_markdown)

        except:
            print("Something went wrong, are you connected?")
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
            chat_id = chat_id_prompt()
    else:
        chat_id = chat_id_prompt()

    message_type = message_type_prompt()
    print("You are going to send {} message to chat id: {}".format(message_type, chat_id))
    if message_type == "sticker":
        sticker_prompt(chat_id)
    elif message_type == "text":
        text_prompt(chat_id, None)
    else:
        print("ERROR: MESSAGE_TYPE_INVALID")


master(None)