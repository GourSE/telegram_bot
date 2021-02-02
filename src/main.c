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

int getLocalConfig();

#endif


int launchScript(int mode);


int main(int argc, char **argv)
{

    int r;
    char flg[50];

    for (r = 0; r < argc; r++)
    {
        if (r == 0)
        {
            strcpy(flg, "*noFlag");
        }
        else if (r == 1)
        {
            strcpy(flg, argv[1]);
        }
        else if (r > 1)
        {
            printf("usage: telegram_bot <-f/-p/-s>\n\n");
            // printf("usage: telegram_bot <single argument value>\n");
            return 1;
        }
    }

    if (strcmp(flg, "-f") == 0)
    {
        printf("telegram bot\n\n");
        launchScript(1);
        return 0;
    }        
    else if (strcmp(flg, "-p") == 0)
    {
        printf("message pusher\n\n");
        launchScript(2);
        return 0;
    }
    else if (strcmp(flg, "-s") == 0)
    {
        printf("support bot\n\n");
        launchScript(3);
        return 0;
    }
    else if (strcmp(flg, "--config") == 0)
    {
        #ifdef __linux__
        char command[150];

        int built = getLocalConfig();

        if (built == -1)
        {
            system("nano config.cfg");
        }
        else
        {
            char *homeDir = getenv("HOME");
            char file_[] = "/.local/share/telegram_bot/config.cfg";
            char *fileLoc = malloc(strlen(homeDir) + strlen(file_) + 1);
            strcpy(fileLoc, homeDir);
            strcat(fileLoc, file_);

            sprintf(command, "%s %s", "nano", fileLoc);
            system(command);
        }
        return 0;
        #else
        ;
        #endif
    }
    else if (strcmp(flg, "-c") == 0)
    {
        #ifdef __linux__
        char command[150];

        int built = getLocalConfig();

        if (built == -1)
        {
            system("nano config.cfg");
        }
        else
        {
            char *homeDir = getenv("HOME");
            char file_[] = "/.local/share/telegram_bot/config.cfg";
            char *fileLoc = malloc(strlen(homeDir) + strlen(file_) + 1);
            strcpy(fileLoc, homeDir);
            strcat(fileLoc, file_);

            sprintf(command, "%s %s", "nano", fileLoc);
            system(command);
        }
        return 0;
        #else
        ;
        #endif
    }
    else if (strcmp(flg, "*noFlag") == 0)
    {
        ;
    }
    else
    {
        printf("'%s' not recognised\n", flg);
        printf("usage: telegram_bot <-f/-p/-s>\n\n");

        return 0;
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


int launchScript(int mode)
{
    #ifdef __linux__

    int built = getLocalConfig();

    if (built == -1)
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
    return 0;
}


#ifdef __linux__

int getLocalConfig()
{
    char *homeDir = getenv("HOME");

    char file_[] = "/.local/share/telegram_bot/config.cfg";

    char *fileLoc = malloc(strlen(homeDir) + strlen(file_) + 1);
    strcpy(fileLoc, homeDir);
    strcat(fileLoc, file_);

    struct stat buffer;
    int file__ = stat(fileLoc, &buffer);

    if (file__ == 0)
    {
        return 0;
    }
    else
    {
        return -1;
    }
    return 0;
}

#endif