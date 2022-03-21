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

# GENERATE SETTINGS
if not os.path.exists("settings.txt"):
    with open('settings.txt', 'w') as whitelist:
        whitelist.write('erase_me_and_put_BOT_TOKEN\n')
        whitelist.write('erase_me_and_put_SAVE_PATH\n')
settings = open("settings.txt").readlines()
settings = [i.strip('\n') for i in settings]
token = settings[0]
save_path = settings[1]


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
        bot.send_message(message.chat.id,
                         "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
        # LOGGING
        print(message.from_user.username + " no auth (text)")


# SAVE PHOTO HANDLER
@bot.message_handler(content_types=["photo"])
def get_photo(message):
    # CHECK WHITELIST
    if message.from_user.username in users:
        # TRY GET PHOTO ORIGINAL SIZE
        try:
            raw = message.photo[3].file_id
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(filename(message.from_user.username, message.message_id, ".jpg", True), 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, "Фотография загружена")
            print("New photo: " + filename(message.from_user.username, message.message_id, ".jpg", True))
        except:
            # TRY GET PHOTO MAXIMUM SIZE
            try:
                raw = message.photo[2].file_id
                file_info = bot.get_file(raw)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(filename(message.from_user.username, message.message_id, ".jpg", True), 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.send_message(message.chat.id, "Фотография загружена")
                print("New photo: " + filename(message.from_user.username, message.message_id, ".jpg", True))
            except:
                # IF FAILED, TRY GET PHOTO MEDUIM SIZE
                try:
                    raw = message.photo[1].file_id
                    file_info = bot.get_file(raw)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(filename(message.from_user.username, message.message_id, ".jpg", True), 'wb') as new_file:
                        new_file.write(downloaded_file)
                    bot.send_message(message.chat.id, "Фотография загружена")
                    print("New meduim photo: " + filename(message.from_user.username, message.message_id, ".jpg", True))
                except:
                    # IF FAILED, TRY GET PHOTO MINIMUM SIZE
                    try:
                        raw = message.photo[0].file_id
                        file_info = bot.get_file(raw)
                        downloaded_file = bot.download_file(file_info.file_path)
                        with open(filename(message.from_user.username, message.message_id, ".jpg", True),
                                  'wb') as new_file:
                            new_file.write(downloaded_file)
                        bot.send_message(message.chat.id, "Фотография загружена")
                        print("New small photo: " + filename(message.from_user.username, message.message_id, ".jpg",
                                                             True))
                    # REPORT IF FAILED
                    except:
                        bot.send_message(message.chat.id, "Ошибка загрузки фотографии (" + str(
                            message.message_id) + "), попробуйте еще раз")
                        print('ERROR:\n', traceback.format_exc())
                        # bot.send_message(message.chat.id, message)
    else:
        bot.send_message(message.chat.id,
                         "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
        # LOGGING
        print(message.from_user.username + " no auth (photo)")


# SAVE VIDEO HANDLER
@bot.message_handler(content_types=["video"])
def get_video(message):
    # CHECK WHITELIST
    if message.from_user.username in users:
        try:
            raw = message.video.file_id
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(filename(message.from_user.username, message.message_id, ".mp4", True), 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, "Видео загружено")
            print("New video: " + filename(message.from_user.username, message.message_id, ".mp4", True))
        except:
            bot.send_message(message.chat.id, "Ошибка загрузки видео (" + str(
                message.message_id) + "), попробуйте еще раз")
            print('ERROR:\n', traceback.format_exc())
    else:
        bot.send_message(message.chat.id,
                         "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
        # LOGGING
        print(message.from_user.username + " no auth (video)")


# SAVE DOCUMENTS HANDLER
@bot.message_handler(content_types=["document"])
def get_document(message):
    # CHECK WHITELIST
    if message.from_user.username in users:
        try:
            raw = message.document.file_id
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(
                    filename(message.from_user.username, message.message_id, ("_" + message.document.file_name), True),
                    'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, "Файл загружен")
            print("New file: " + filename(message.from_user.username, message.message_id,
                                          ("_" + message.document.file_name), False))
        except:
            bot.send_message(message.chat.id, "Ошибка загрузки документа (" + str(
                message.message_id) + "), попробуйте еще раз")
            print('ERROR:\n', traceback.format_exc())

    else:
        bot.send_message(message.chat.id,
                         "Неизвестный пользователь: " + message.from_user.username + "\nОбратитесь к администратору")
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
