## Welcome to FileBotTG 1.0

This script allows you to upload files to your local drive. 
Just send a message containing a photo, video or document to the configured bot and it will download it 

The feature is the save path in the format:
PATH_TO_SAVE_FILES\date\username\all files per day
This feature is subject to change/improvement. 

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
