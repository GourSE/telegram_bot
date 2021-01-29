#-*- Makefile -*-

all: telegram_bot

telegram_bot: src/main.c
	gcc src/main.c -o ~/.local/bin/telegram_bot
	mkdir -p ~/.local/share/telegram_bot
	cp -r -u ./*.py ./config.cfg ~/.local/share/telegram_bot
	pip3 install -r requirements.txt -U
	echo "\nRemember to update config.cfg if modified, by running make\nto remove program, use 'make clean'\n"

to_current: src/main.c
	gcc src/main.c -o telegram_bot

clean:
	rm -f ~/.local/bin/telegram_bot
	rm -f -r ~/.local/share/telegram_bot
	rm -f telegram_bot