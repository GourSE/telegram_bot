# coding=utf-8

import platform

class colour:
    this__os = platform.system()
    if this__os == "Windows":
        reset   = "\033[0m"

        # normal colours
        black   = "\033[30m"
        red     = "\033[31m"
        green   = "\033[32m"
        yellow  = "\033[33m"
        blue    = "\033[34m"
        magenta = "\033[35m"
        cyan    = "\033[36m"

        # bold colours
        BLACK   = "\033[01m\033[30m"
        RED     = "\033[01m\033[31m"
        GREEN   = "\033[01m\033[32m"
        YELLOW  = "\033[01m\033[33m"
        BLUE    = "\033[01m\033[34m"
        MAGENTA = "\033[01m\033[35m"
        CYAN    = "\033[01m\033[36m"
        
        # costum styles
        WARNING = "\033[01m\033[01m\033[31m"
        BOLD    = "\033[01m"
            # this is black text with white bg
        WHITE   = "\033[30m\033[40m"
        
    else:

        reset   = "\033[0;0m"

        # normal colours
        black   = "\033[0;30m"
        red     = "\033[0;31m"
        green   = "\033[0;32m"
        yellow  = "\033[0;33m"
        blue    = "\033[0;34m"
        magenta = "\033[0;35m"
        cyan    = "\033[0;36m"

        # bold colours
        BLACK   = "\033[1;30m"
        RED     = "\033[1;31m"
        GREEN   = "\033[1;32m"
        YELLOW  = "\033[1;33m"
        BLUE    = "\033[1;34m"
        MAGENTA = "\033[1;35m"
        CYAN    = "\033[1;36m"
        
        # costum styles
        WARNING = "\033[1;37;41m"
        BOLD    = "\033[;1m"
            # this is black text with white bg
        WHITE   = "\033[1;30;47m"


# print(f"{colour.YELLOW}hello, world{colour.reset} ")