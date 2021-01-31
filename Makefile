#-*- Makefile -*-

ifeq ($(OS),Windows_NT) 
	detected_OS := Windows
	CC ?= gcc
else
	detected_OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')

ifeq (, $(shell which gcc))
	CC = clang
else ifeq (, $(shell which clang))
	CC = gcc
else ifeq (, $(shell which cc))

all: error

endif

endif

all: telegram_bot

ifeq ($(detected_OS), Linux)

telegram_bot: src/main.c

	$(CC) src/main.c -o ~/.local/bin/telegram_bot
	mkdir -p ~/.local/share/telegram_bot
	cp -r -u ./*.py ./config.cfg ~/.local/share/telegram_bot

ifeq (, $(shell which pip3))
	pip install -r requirements.txt -U
else
	pip3 install -r requirements.txt -U
endif

	@echo "\ndone"
	@echo "Remember to update config.cfg if modified, by running 'make'"
	@echo "To compile into this directory, run 'make current_dir'"
	@echo "To remove program, run 'make clean'\n"

current_dir: src/main.c
	$(CC) src/main.c -o telegram_bot

	@echo "\ndone"

clean:
	rm -f ~/.local/bin/telegram_bot
	rm -f -r ~/.local/share/telegram_bot
	rm -f telegram_bot

	@echo "\ndone"

endif

ifeq ($(detected_OS), Windows)

telegram_bot: src\main.c
	if not exist %ProgramFiles(x86)%\GourSE mkdir %ProgramFiles(x86)%\GourSE
	if not exist %ProgramFiles(x86)%\GourSE\telegram_bot mkdir %ProgramFiles(x86)%\GourSE\telegram_bot
	
	$(CC) /Fe"%ProgramFiles(x86)%\GourSE\telegram_bot\telegram_bot.exe" src\main.c
	
	copy %CD%\*.py %ProgramFiles(x86)%\GourSE\telegram_bot\
	copy %CD%\config.cfg %ProgramFiles(x86)%\GourSE\telegram_bot\
	copy %CD%\src\images\icon.ico %ProgramFiles(x86)%\GourSE\telegram_bot\


	set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
	echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
	echo sLinkFile = "%USERPROFILE%\Desktop\Telegram Bot.lnk" >> %SCRIPT%
	echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
	echo oLink.TargetPath = "%ProgramFiles(x86)%\GourSE\telegram_bot\telegram_bot.exe" >> %SCRIPT%
	echo oLink.Arguments = "-h ServerNameOrIP -a ifix" >> %SCRIPT%
	echo oLink.IconLocation = "%ProgramFiles(x86)%\GourSE\telegram_bot\icon.ico" >> %SCRIPT%
	echo oLink.Save >> %SCRIPT%
	cscript /nologo %SCRIPT%
	del %SCRIPT%

	@echo "\ndone."
	@echo "Remember to update config.cfg if modified, by running 'make.exe'"
	@echo "To compile into this directory, run 'make.exe current_dir'"
	@echo "To remove program, run 'make.exe clean'\n"

current_dir: src\main.c

	$(CC) /Fe"%CD%\telegram_bot.exe" src\main.c

	set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
	echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
	echo sLinkFile = "%USERPROFILE%\Desktop\Telegram Bot.lnk" >> %SCRIPT%
	echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
	echo oLink.TargetPath = "%CD%\telegram_bot.exe" >> %SCRIPT%
	echo oLink.Arguments = "-h ServerNameOrIP -a ifix" >> %SCRIPT%
	echo oLink.IconLocation = "%CD%\src\images\icon.ico" >> %SCRIPT%
	echo oLink.Save >> %SCRIPT%
	cscript /nologo %SCRIPT%
	del %SCRIPT%

	@echo "\ndone"

clean:
	if exist %ProgramFiles(x86)%\GourSE\telegram_bot rmdir /Q /S %ProgramFiles(x86)%\GourSE\telegram_bot
	if exist "%USERPROFILE%\Desktop\Telegram Bot.lnk" del /f "%USERPROFILE%\Desktop\Telegram Bot.lnk"
	if exist "%CD%\telegram_bot.exe" del \f "%CD%\telegram_bot.exe"

	@echo "\ndone"

endif

error:
	@echo "No compiler installed"
	$(error "No compiler installed")