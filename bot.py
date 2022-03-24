import os
import sys
import traceback
from datetime import date, datetime

import telebot

# VAR
users = []
settings = []
token = ""
save_path = "C:/img/"
notifications = 1

# GENERATE SETTINGS
if not os.path.exists("settings.txt"):
    with open('settings.txt', 'w') as whitelist:
        whitelist.write('erase_me_and_put_BOT_TOKEN\n')
        whitelist.write('erase_me_and_put_SAVE_PATH\n')
        whitelist.write('1\n')
settings = open("settings.txt").readlines()
settings = [i.strip('\n') for i in settings]
token = settings[0]
save_path = settings[1]
notifications = int(settings[2])

# GENERATE WHITELIST
if not os.path.exists("whitelist.txt"):
    with open('whitelist.txt', 'w') as whitelist:
        whitelist.write('erase_me_and_put_users_one_per_line\n')
users = open("whitelist.txt").readlines()
users = [i.strip('\n') for i in users]


# GENERATE PATH+FNAME
def filename(user_id, mess_id, ext, save):
    global save_path
    now = datetime.now()
    current_time = now.strftime("%H.%M.%S")
    date_path = save_path + str(date.today())
    user_path = date_path + "/" + user_id
    if save:
        if not os.path.exists(date_path):
            os.makedirs(date_path)
        if not os.path.exists(user_path):
            os.makedirs(user_path)

    fname = user_path + "/" + current_time + "_" + str(mess_id) + ext
    return fname


# REPLY NOTIFIER
def notify(chat_id, message_id, media_type, status):
    if notifications:
        if media_type == "video":
            if status:
                bot.send_message(chat_id, "Видео загружено")
            else:
                bot.send_message(chat_id, "Ошибка загрузки видео (" + str(message_id) + "), попробуйте еще раз")

        if media_type == "photo":
            if status:
                bot.send_message(chat_id, "Фото загружено")
            else:
                bot.send_message(chat_id, "Ошибка загрузки фото (" + str(message_id) + "), попробуйте еще раз")

        if media_type == "document":
            if status:
                bot.send_message(chat_id, "Документ загружен")
            else:
                bot.send_message(chat_id, "Ошибка загрузки документа (" + str(message_id) + "), попробуйте еще раз")


# GET FILE
def get_file(file_id):
    raw = file_id
    file_info = bot.get_file(raw)
    return bot.download_file(file_info.file_path)


# INIT BOT
bot = telebot.TeleBot(token)


# REPLY TEXT HANDLER
@bot.message_handler(content_types=["text"])
def get_text(message):
    # CHECK WHITELIST
    if message.from_user.username in users:
        bot.send_message(message.chat.id, "Ok")
        # LOGGING
        print(message.from_user.username + " send text:")
        print(message.text)
    else:
        bot.send_message(message.chat.id, "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
        # LOGGING
        print(message.from_user.username + " no auth (text)")


# SAVE PHOTO HANDLER
@bot.message_handler(content_types=["photo"])
def get_photo(message):
    # CHECK WHITELIST
    if message.from_user.username in users:
        # TRY GET PHOTO ORIGINAL SIZE
        try:
            with open(filename(message.from_user.username, message.message_id, ".jpg", True), 'wb') as new_file:
                new_file.write(get_file(message.photo[3].file_id))
            notify(message.chat.id, message.message_id, "photo", True)
            print("New photo: " + filename(message.from_user.username, message.message_id, ".jpg", True))
        except:
            # TRY GET PHOTO MAXIMUM SIZE
            try:
                with open(filename(message.from_user.username, message.message_id, ".jpg", True), 'wb') as new_file:
                    new_file.write(get_file(message.photo[2].file_id))
                notify(message.chat.id, message.message_id, "photo", True)
                print("New photo: " + filename(message.from_user.username, message.message_id, ".jpg", True))
            except:
                # IF FAILED, TRY GET PHOTO MEDIUM SIZE
                try:
                    with open(filename(message.from_user.username, message.message_id, ".jpg", True), 'wb') as new_file:
                        new_file.write(get_file(message.photo[1].file_id))
                    notify(message.chat.id, message.message_id, "photo", True)
                    print("New meduim photo: " + filename(message.from_user.username, message.message_id, ".jpg", True))
                except:
                    # IF FAILED, TRY GET PHOTO MINIMUM SIZE
                    try:
                        with open(filename(message.from_user.username, message.message_id, ".jpg", True),
                                  'wb') as new_file:
                            new_file.write(get_file(message.photo[0].file_id))
                        notify(message.chat.id, message.message_id, "photo", True)
                        print("New small photo: " + filename(message.from_user.username, message.message_id, ".jpg", True))
                    # REPORT IF FAILED
                    except:
                        notify(message.chat.id, message.message_id, "photo", False)
                        print('ERROR:\n', traceback.format_exc())
    else:
        bot.send_message(message.chat.id, "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
        print(message.from_user.username + " no auth (photo)")


# SAVE VIDEO HANDLER
@bot.message_handler(content_types=["video"])
def get_video(message):
    if message.from_user.username in users:
        try:
            with open(filename(message.from_user.username, message.message_id, ".mp4", True), 'wb') as new_file:
                new_file.write(get_file(message.video.file_id))
            notify(message.chat.id, message.message_id, "video", True)
            print("New video: " + filename(message.from_user.username, message.message_id, ".mp4", True))
        except:
            notify(message.chat.id, message.message_id, "video", False)
            print('ERROR:\n', traceback.format_exc())
    else:
        bot.send_message(message.chat.id, "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
        print(message.from_user.username + " no auth (video)")


# SAVE DOCUMENTS HANDLER
@bot.message_handler(content_types=["document"])
def get_document(message):
    # CHECK WHITELIST
    if message.from_user.username in users:
        try:
            with open(filename(message.from_user.username, message.message_id, ("_" + message.document.file_name), True), 'wb') as new_file:
                new_file.write(get_file(message.document.file_id))
            notify(message.chat.id, message.message_id, "document", True)
            print("New file: " + filename(message.from_user.username, message.message_id, ("_" + message.document.file_name), False))
        except:
            notify(message.chat.id, message.message_id, "document", False)
            print('ERROR:\n', traceback.format_exc())
    else:
        bot.send_message(message.chat.id, "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
        # LOGGING
        print(message.from_user.username + " no auth (document)")


# STARTING BOT
print("Welcome to FileBotTG 1.0")
print("\nCurrent settings:")
print(settings)
print("\nExample filepath:")
print(filename("username", "message_id", ".jpg", False))
print("\nAccess granted users:")
print(users)
print("\nStarting bot...\n")
try:
    bot.polling(none_stop=True)
except:
    print('ERROR:\n', traceback.format_exc())
    sys.exit(0)
