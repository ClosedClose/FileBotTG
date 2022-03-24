## Welcome to FileBotTG 1.0

This script allows you to upload files to your local drive. 
Just send a message containing a photo, video or document to the configured bot and it will download it 

Files are saved in the following format:
```
PATH_TO_SAVE_FILES\date\username\all files per day
```
This feature is subject to change or improvement. 


This script has a whitelist by Telegram username, don't forget to add yourself to the list 

### Usage

Requires pyTelegramBotAPI:
```
pip install pyTelegramBotAPI
```

Fill "settings.txt" with the settings:
```
BOT_TOKEN 
PATH_TO_SAVE_FILES
NOTIFICATIONS
```

Fill "whitelist.txt" with the settings:
```
USERNAME1
USERNAME2
etc
```
"settings.txt" and "whitelist.txt" should be filled line by line with no comments

![cover](/cover.png)
