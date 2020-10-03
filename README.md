# Telegram bot api message pusher

> simple script for you to push message with your bot using Telegram bot API


### ***To run the script***

- install python

- put your bot token in 'config.cfg'

- install modules in 'requirements.txt'

- run 'message_pusher.py'

### ***Tips***

while the script asking you for the text and the sticker ID, you can type ***:q*** to restart script

you can choose to send typing action to chat by changing 'config.cfg' under [settings] > [send_typing], the default is set to True

you can also choose to use markdown from 'config.cfg' under [settings] > [use_markdown], the default is set to False

------------


# Telegram support bot

> script for setting up a support bot


### ***To run the script***

- install python

- put your bot token in 'config.cfg'

- put admin chat ID or user ID in 'config.cfg' under [settings] > [admin_id]

- install modules in 'requirements.txt'

- run 'support_bot.py'

### ***How does it work***

if a user send a message to the bot, it'll forward it to the chat ID you inserted in 'config.cfg'

the chat ID can be both your own user ID(your user ID is your chat ID) or a group chat ID

to reply to the user, you simply reply to the forwared message

your message will be sent to the user directly