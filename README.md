
|![alt text](https://raw.githubusercontent.com/ClosedClose/FileBotTG/refs/heads/main/icons/icon_48.png)| ## Welcome to FileBotTG 1.2|

This script allows you to upload files to your local drive. 
Just send a message containing a photo, video or document to the configured bot and it will download it 

Files are saved in the following format:
```
PATH_TO_SAVE_FILES\date\username\*all files per day*
```
This feature is subject to change or improvement. 


This script has a whitelist by Telegram username, don't forget to add yourself to the whitelist.txt 

### Usage

Run "install.bat", script will download all requirements (pip, ffmpeg, yt-dlp) 

Fill "settings.txt" with the settings:
```
BOT_TOKEN 
PATH_TO_SAVE_FILES
NOTIFICATIONS
```

Fill "whitelist.txt" with usernames of admin(s):
```
USERNAME1
USERNAME2
etc
```
"settings.txt" and "whitelist.txt" should be filled line by line with no comments

Run "run.bat"

![cover](/cover.png)




