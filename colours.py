# coding=utf-8

class colour:
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