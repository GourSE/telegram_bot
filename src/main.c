#ifdef _WIN32

#include <Windows.h>
#include <stdio.h>
#include <tchar.h>
#define DIV 1048576 
#define WIDTH 7

const char TELEGRAM_BOT[] = "python telegram_bot.py";
const char MESSAGE_PUSHER[] = "python message_pusher.py";
const char SUPPORT_BOT[] = "python support_bot.py";

#elif __APPLE__

#include <TargetConditionals.h>

const char TELEGRAM_BOT[] = "python telegram_bot.py";
const char MESSAGE_PUSHER[] = "python message_pusher.py";
const char SUPPORT_BOT[] = "python support_bot.py";

#elif __linux__

#define _PROGRAM_NAME "Telegram Bot"
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

const char TELEGRAM_BOT_C[] = "python3 telegram_bot.py";
const char MESSAGE_PUSHER_C[] = "python3 message_pusher.py";
const char SUPPORT_BOT_C[] = "python3 support_bot.py";

const char TELEGRAM_BOT[] = "python3 ~/.local/share/telegram_bot/telegram_bot.py";
const char MESSAGE_PUSHER[] = "python3 ~/.local/share/telegram_bot/message_pusher.py";
const char SUPPORT_BOT[] = "python3 ~/.local/share/telegram_bot/support_bot.py";


#endif


int launchScript(int mode)
{
    #ifdef __linux__
    // FILE    *fp;

    // fp = popen("file telegram_bot", "r");
    // printf("%s" ,fp);

    char *homeDir = getenv("HOME");

    char file_[] = "/.local/share/telegram_bot/config.cfg";

    char *fileLoc = malloc(strlen(homeDir) + strlen(file_) + 1);
    strcpy(fileLoc, homeDir);
    strcat(fileLoc, file_);

    // debug
    // printf("%s\n", fileLoc);

    struct stat buffer;
    int file__ = stat(fileLoc, &buffer);

    if (file__ == -1)
    {
        // debug
        // printf("no\n");
        
        switch (mode)
        {
            case 1:
                system(TELEGRAM_BOT_C);
                return 0;
            
            case 2:
                system(MESSAGE_PUSHER_C);
                return 0;

            case 3:
                system(SUPPORT_BOT_C);
                return 0;
        }
    }
    else
    {
        switch (mode)
        {
            case 1:
                system(TELEGRAM_BOT);
                return 0;
            
            case 2:
                system(MESSAGE_PUSHER);
                return 0;

            case 3:
                system(SUPPORT_BOT);
                return 0;
        }
    }
    #else
    switch (mode)
    {
        case 1:
            system(TELEGRAM_BOT);
            return 0;
        
        case 2:
            system(MESSAGE_PUSHER);
            return 0;

        case 3:
            system(SUPPORT_BOT);
            return 0;
    }
    #endif
}


int main(int argc, char **argv)
{
    int r;
    char flg;

    for (r = 0; r < argc; r++)
        if (r == 1)
        {
            flg = argv[1][1];
        }
        else
        {
            flg = '0';
        }

    switch (flg)
    {
        case 'f':
            printf("telegram bot\n\n");
            launchScript(1);
            return 0;
            
        case 'p':
            printf("message pusher\n\n");
            launchScript(2);
            return 0;

        case 's':
            printf("support bot\n\n");
            launchScript(3);
            return 0;

        default:
            break;
    }

    while(1)
    {
        char mode[30];
        printf("select script to run\n\n1. telegram bot:\n\tfully featured telegram bot\n\tinteract with bot in Telegram\n\tsend dms and group messages\n\tsend text and stickers\n\treply to users\n\tsend media\n\n2. message pusher:\n\tinteract with bot in terminal/cmd\n\tsend dms and group messages\n\tsend text and stickers\n\n3. support bot:\n\tinteract with bot in Telegram\n\tsend text and stickers\n\treply to users\n\tsend media\n\ncheck README for more info\n\ntelegram_bot > $ ");
        scanf("%s", mode);
        switch (mode[0])
        {
            case '1':
                #ifdef _WIN32
                system("cls");
                #else
                system("clear");
                #endif

                printf("telegram bot selected\n\n");
                launchScript(1);
                return 0;
                break;
            
            case '2':
                #ifdef _WIN32
                system("cls");
                #else
                system("clear");
                #endif

                printf("message pusher selected\n\n");
                launchScript(2);
                return 0;
                break;

            case '3':
                #ifdef _WIN32
                system("cls");
                #else
                system("clear");
                #endif

                printf("support bot selected\n\n");
                launchScript(3);
                return 0;
                break;

            case 'q':
                return 0;

            default:
                printf("\n\n%s is not a mode\n", mode);
                sleep(1);

                #ifdef _WIN32
                system("cls");
                #else
                system("clear");
                #endif

                printf("%s is not a mode\n", mode);
                break;
        }
    }
}