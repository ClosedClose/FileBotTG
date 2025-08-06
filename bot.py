import os
import sys
import re
import traceback
import subprocess
from datetime import date, datetime
import random
from pathlib import Path

import telebot
from telebot.types import ReactionTypeEmoji

import sqlite3
import requests
import bs4

db_path = "filebot_users.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    date_joined TEXT
)
""")

version= "1.2"

conn.commit()

def getAnekdot():
    url = 'https://anekdot.ru/random/anekdot'                        
    h   = {"User-Agent":"1"}                   # сайт не пускает без header
    web = requests.get(url, headers=h).text    # Получение кода веб-сайта, где расположены случайные анекдоты
    bs      = bs4.BeautifulSoup(web, "html.parser")                             
    result    = str(bs.find_all(class_="topicbox")[1].find(class_="text"))  # получаем элемент, в котором написан текст анекдота
    text = result.replace("<br/>","\n")                           # удаляем лишние теги, которые попали в наш текст. заменяем тег переноса на \n
    text = text.split(">")
    text[0] = ""
    text = ''.join(text)
    text = text.split("<")
    text[-1] = ""
    text = ''.join(text)
    return text

platform = sys.platform
if platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleCP(65001)
    kernel32.SetConsoleOutputCP(65001)

def load_settings():
    settings_path = Path("settings.txt")
    if not settings_path.exists():
        settings_path.write_text("erase_me_and_put_BOT_TOKEN\nerase_me_and_put_SAVE_PATH\n1\n")
    lines = settings_path.read_text().splitlines()
    token = lines[0]
    save_path = Path(lines[1])
    notifications = int(lines[2])
    return token, save_path, notifications


def load_users():
    whitelist_path = Path("whitelist.txt")
    if not whitelist_path.exists():
        whitelist_path.write_text("erase_me_and_put_users_one_per_line\n")
    return whitelist_path.read_text().splitlines()


# Initialize configuration and bot
token, save_path, notifications = load_settings()
users = load_users()
bot = telebot.TeleBot(token)


def create_filepath(user_id, mess_id, ext, do_create=True):
    now_str = datetime.now().strftime("%H.%M.%S")
    date_dir = save_path / str(date.today())
    user_dir = date_dir / user_id
    if do_create:
        user_dir.mkdir(parents=True, exist_ok=True)
    return str(user_dir / f"{now_str}_{mess_id}{ext}")


def notify(chat_id, message_id, media_type, status):
    messages = {
        "video": ("Видео загружено", f"Ошибка загрузки видео ({message_id}), попробуйте еще раз"),
        "photo": ("Фото загружено", f"Ошибка загрузки фото ({message_id}), попробуйте еще раз"),
        "document": ("Документ загружен", f"Ошибка загрузки документа ({message_id}), попробуйте еще раз"),
        "yt": (f"Видео YT загружено: {message_id}", f"Ошибка загрузки YT ({message_id}), попробуйте еще раз"),
    }
    text = messages.get(media_type, ("", ""))[0 if status else 1]
    bot.send_message(chat_id, text)
    if media_type == "yt" and status:
        print("New YT:", message_id)


def verify_user(message):
    if message.from_user.username in users:
        return True
    print(f"\n{message.from_user.username} no auth (verify)")
    # Determine the target user: if the message is a reply, forwarded, or from a channel/bot,
    # use the original author's data; otherwise, use the message sender's data.
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user
    elif getattr(message, "forward_from", None):
        target = message.forward_from
    elif getattr(message, "sender_chat", None):
        target = message.sender_chat
    else:
        target = message.from_user

    # Use 'title' as username if no username exists (e.g. for channel messages)
    username = target.username if hasattr(target, "username") and target.username else getattr(target, "title", "Unknown")
    user_id = getattr(target, "id", "Unknown")
    first_name = getattr(target, "first_name", "")
    last_name = getattr(target, "last_name", "")

    bot.send_message(
        message.chat.id,
        f"Unauthorized access attempt detected.\n"
        f"Username: {username}\n"
        f"User ID: {user_id}\n"
        f"First Name: {first_name}\n"
        f"Last Name: {last_name}"
    )

    return False


def get_file(file_id):
    file_info = bot.get_file(file_id)
    return bot.download_file(file_info.file_path)


def send_reaction(message, emoji_code):
    bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(emoji_code)], is_big=False)


def send_succeed_reaction(message):
    send_reaction(message, "\U0001F44D")


def send_failed_reaction(message):
    send_reaction(message, "\U0001F44E")

@bot.message_handler(commands=["start"])
def handle_start(message):  
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("ping", "yt", "help")

    # Store new user in SQLite3 database
    username = message.from_user.username
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (username, first_name, last_name, date_joined) VALUES (?, ?, ?, ?)",
            (username, first_name, last_name, date_joined)
        )
        conn.commit()

    if not verify_user(message):
        bot.send_message(
            message.chat.id,
            f"Неизвестный пользователь (Первый запуск!): {username}\n"
        )
        return
    bot.send_message(message.chat.id, "Добро пожаловать в FileBotTG 1.0!\nНапишите /help для получения списка команд.", reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if verify_user(message):
        
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("ping", "yt", "help")
    
        if "https" in message.text:
            bot.send_message(message.chat.id, "Обнаружена ссылка")
            # Extract individual YouTube URLs even if they are concatenated together
            pattern = r'(https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/)[\w-]+|youtu\.be/[\w-]+)[^\s]*)'
            yt_urls = re.findall(pattern, message.text)
            if not yt_urls:
                notify(message.chat.id, "Unknown URL", "yt", False)
                return

            for yt_url in yt_urls:
                try:
                    print("Detected YouTube URL")

                    # Create the output folder for today's videos
                    date_folder = save_path / str(date.today())
                    date_folder.mkdir(parents=True, exist_ok=True)
                    output_template = str(date_folder / "%(title)s-%(id)s.%(ext)s")

                    result = subprocess.run(
                        ["yt-dlp.exe", "-i", "-o", output_template, yt_url],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if result.returncode == 0 or "has already been downloaded" in result.stdout:
                        print("yt-dlp download succeeded! (" + str(result.returncode) + ")")
                        send_reaction(message, "\U0001F44D")
                    else:
                        print("yt-dlp download failed! (" + str(result.returncode) + ")")
                        send_reaction(message, "\U0001F44E")
                except Exception as error:
                    print("Error in yt-dlp download:", error)
                    notify(message.chat.id, yt_url, "yt", False)

        if "ping" in message.text and verify_user(message):
            bot.send_message(message.chat.id, "Pong!")

        if "help" in message.text and verify_user(message):
            help_text = (
                "FileBotTG 1.0\n"
                "\n"
                "Available commands:\n"
                "/start - Start the bot\n"
                "/help - Show this help message\n"
                "/ping - Check if the bot is alive\n"
                "/random - Get a random number\n"
                "/date - Get the current date\n"
                "/time - Get the current time\n"
                "/users - List current users\n"
                "/settings - Show bot settings\n"
                "/anek - Show random anekdot\n"
                "\n"
                "Send text, photos, videos, or documents to save them.\n"
                "You can also send YouTube links for downloading."
            )
            bot.send_message(message.chat.id, help_text)

        if "yt" in message.text and verify_user(message):
            if platform == "win32":
                result = subprocess.run(["ping", "-n", "1", "youtube.com"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    bot.send_message(message.chat.id, "Ping to youtube.com succeeded")
                else:
                    bot.send_message(message.chat.id, "Ping to youtube.com failed")
            else:
                result = subprocess.run(
                    ["ping", "-c", "1", "youtube.com"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0:
                    bot.send_message(message.chat.id, "Ping to youtube.com succeeded")
                else:
                    bot.send_message(message.chat.id, "Ping to youtube.com failed")

        if "random" in message.text and verify_user(message):
            random_number = random.randint(1, 100)
            bot.send_message(message.chat.id, f"Random number: {random_number}")

        if "date" in message.text and verify_user(message):
            current_date = date.today().strftime("%Y-%m-%d")
            bot.send_message(message.chat.id, f"Current date: {current_date}") 

        if "time" in message.text and verify_user(message):
            current_time = datetime.now().strftime("%H:%M:%S")
            bot.send_message(message.chat.id, f"Current time: {current_time}")
        
        if "users" in message.text and verify_user(message):
            cursor.execute("SELECT id, username, first_name, last_name, date_joined FROM users ORDER BY date_joined DESC LIMIT 10")
            user_list = cursor.fetchall()
            total_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

            if user_list:
                users_info = "\n".join([
                    f"ID: {user[0]}, Username: {user[1]}, First Name: {user[2]}, Last Name: {user[3]}, Joined: {user[4]}"
                    for user in user_list
                ])
                bot.send_message(message.chat.id, f"Total users: " + str(total_users))
                bot.send_message(message.chat.id, f"Current users:\n{users_info}")
            else:
                bot.send_message(message.chat.id, "No users found.")
        
        if "admins" in message.text and verify_user(message):
            users_list = "\n".join(users)
            bot.send_message(message.chat.id, f"Current users:\n{users_list}")

        if "settings" in message.text and verify_user(message):
            settings_info = (
                f"Platform: {platform}\n"
                f"Token: *****\n"
                f"Save Path: {save_path}\n"
                f"Notifications: {'Enabled' if notifications else 'Disabled'}\n"
                f"Users: {', '.join(users)}\n"
            )
            bot.send_message(message.chat.id, settings_info)

        if "anek" in message.text and verify_user(message):
            anek = getAnekdot()
            bot.send_message(message.chat.id, anek, reply_markup=keyboard)
        
        if "stop" in message.text and verify_user(message):
            bot.send_message(message.chat.id, "Bot is stopping...")
            print("Bot stopped by user request.")
            os._exit(0)   



@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    if not verify_user(message):
        return

    # Try photo sizes from highest to lowest quality
    for photo in reversed(message.photo):
        try:
            file_path = create_filepath(message.from_user.username, message.message_id, ".jpg", do_create=True)
            with open(file_path, 'wb') as new_file:
                new_file.write(get_file(photo.file_id))
            send_succeed_reaction(message)
            print(f"\nNew photo: {file_path}")
            return
        except Exception:
            continue

    send_failed_reaction(message)
    print('\nERROR:\n', traceback.format_exc())


@bot.message_handler(content_types=["video"])
def handle_video(message):
    if verify_user(message):
        try:
            file_path = create_filepath(message.from_user.username, message.message_id, ".mp4", do_create=True)
            with open(file_path, 'wb') as new_file:
                new_file.write(get_file(message.video.file_id))
            send_succeed_reaction(message)
            print(f"\nNew video: {file_path}")
        except Exception:
            send_failed_reaction(message)
            print('\nERROR:\n', traceback.format_exc())


@bot.message_handler(content_types=["document"])
def handle_document(message):
    if verify_user(message):
        try:
            file_ext = "_" + message.document.file_name
            file_path = create_filepath(message.from_user.username, message.message_id, file_ext, do_create=True)
            with open(file_path, 'wb') as new_file:
                new_file.write(get_file(message.document.file_id))
            send_succeed_reaction(message)
            print(f"\nNew file: {file_path}")
        except Exception:
            send_failed_reaction(message)
            print("\nERROR:\n", traceback.format_exc())
    else:
        bot.send_message(
            message.chat.id,
            f"Неизвестный пользователь: {message.from_user.username}\nОбратитесь к администратору"
        )
        print(f"\n{message.from_user.username} no auth (document)")


def main():
    print("Welcome to FileBotTG "+ version + "!\n")
    print("\nCurrent settings:")
    print([str(token), str(save_path), notifications])
    example_filepath = create_filepath("username", "message_id", ".jpg", do_create=False)
    print("\nExample filepath:")
    print(example_filepath)
    print("\nAccess granted users:")
    print(users)
    print("\nStarting bot...\n")

    try:
        bot_info = bot.get_me()
        print(f"\033[32m@{bot_info.username}\033[0m is running\n")
        bot.infinity_polling(allowed_updates=['message', 'message_reaction'], none_stop=True)
    except Exception:
        print("\033[31mERROR\033[0m:\n", traceback.format_exc())
        sys.exit(0)


if __name__ == '__main__':
    main()
