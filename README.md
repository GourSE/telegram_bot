# Telegram bot

> script to push message with your bot, and reply message for your bot, by interacting with the bot

### ***Tips***

- any message sent to the bot will be forward to the admin chat ID you inserted in 'config.cfg'  
  
  the admin chat ID can be both your own user chat ID(your user ID is also your chat ID) or a group chat ID  
  
  to reply to the user, you simply reply to the forwared message  
  
  your message will be sent to the user directly

- to send a message to a chat, you first have to know the chat ID of the user or the group chat ID  
  
  then you'll have to reply to a message with the chat ID like this  

  ![](./images/01.png)  
    
    by that you can send text message, sticker or media to a group chat or user

-------

# Telegram bot api message pusher

> simple script for you to push message with your bot by interacting with the terminal window


### ***Tips***

while the script asking you for the text and the sticker ID, you can type ***:q*** to restart script

you can choose to send typing action to chat by changing 'config.cfg' under [settings] > [send_typing], the default is set to True

you can also choose to use markdown from 'config.cfg' under [settings] > [use_markdown], the default is set to False

------------


# Telegram support bot

> script for setting up a support bot


### ***Tips***

if a user send a message to the bot, it'll forward it to the chat ID you inserted in 'config.cfg'

the chat ID can be both your own user ID(your user ID is your chat ID) or a group chat ID

to reply to the user, you simply reply to the forwared message

your message will be sent to the user directly

# Installing

## Linux
- Install python and pip

  ***Install python with your package manager***

  ***Debian as an example:***

  `sudo apt install python3 python3-pip`


- Install GCC or Clang

  ***Install GCC or Clang with your package manager***

  ***Debian as an example:***

  `sudo apt install gcc`
  
  or

  `sudo apt install clang`

  ***If you can't install them or not looking forward to, skip the next 2 steps***


- Build the program with `make`

  > Must have a compiler installed

  ***Build the program with make***

  ***The program will be built in '.local/share/telegram_bot'***

  `make`

  ***If you want to compile the binary in the project directory, run this command instead***

  `make current_dir`

- Launch the program

  ***Launch the program with the command below***

  `telegram_bot`

  ***and select the script to run***


- Launch with python

  ***To launch directly with python, you will have two step***

  - Install requirements

    > You can skip this step if you already build the program with `make`
    
    ***install them with the command below***

    `pip3 install -r requirements.txt -U`

    ***If you're on CentOS, RHEL or Arch Linux, install with this command instead***

    `pip install -r requirements.txt -U`

    Note that you'll have to be in the project directory

  - Launch the program with python

    ***Choose one of the three scripts***

      - telegram_bot.py

      - message_pusher.py

      - support_bot.py

    ***Launch with the command below***

    `python3 <script>`

    ***or***

    `python <script>`

    ***Take telegram_bot.py as example***

    `python3 telegram_bot.py`

    ***or***

    `python telegram_bot.py`

-------

## Windows
- Open ***cmd*** or ***power shell*** in the project folder

- Install python

  ***Go to [the offical website of Python](https://www.python.org/) to download Python and install with the installer***

- Install requirements

  ***Install them with the command below***

  `pip install -r requirements.txt -U`

- Launch the program with python

  ***Choose one of the three scripts***

    - telegram_bot.py

    - message_pusher.py

    - support_bot.py

  ***Launch with the command below***

  `python <script>`

  ***Take telegram_bot.py for example***

  `python telegram_bot.py`

- Build the project with `make`

  ***If you have GNU Make and GCC installed in your windows PC, use the command below***

  `make`

  ***The program will be installed in your program files and a deskop shortcut will appear***

  ***If you want to remove the program, use the command below***

  `make clean`

- Launch the program

  > You will have to build the program with `make` for this method

  ***Launch the program with the desktop shortcut and select the script to run***