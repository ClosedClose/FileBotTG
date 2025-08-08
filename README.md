### Welcome to FileBotTG 1.3

![alt text](./cover.png)
---

**FileBotTG** is a private, asynchronous Telegram bot designed to download files (photos, videos, documents) sent to it directly to your local drive. With a simple setup and a whitelist for user access, it ensures secure and efficient file management.

## Features
- **Asynchronous Downloads**: Quickly download files sent to the bot (photos, videos, or documents).
- **Whitelist Security**: Only users listed in `whitelist.cfg` can interact with the bot.
- **Reactions**: Feedback with custom reactions defined via `settings.cfg`. (not all works with API)
- **Custom path**: Free to set any output directory (e.g., `C:\Downloads` or `/home/user/downloads`).
- **Easy Setup**: Install dependencies and run the bot with simple batch scripts.

*Note*: File storage structure may be improved or changed in future releases.

## Prerequisites
- Python 3.8+
- Telegram account and a bot token (create via [BotFather](https://t.me/BotFather))
- [FFmpeg](https://ffmpeg.org/) for media processing
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading external media
- CMD (for install scripts) or BASH to setup manually

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ClosedClose/FileBotTG.git
   cd FileBotTG
   ```

2. **Run Installation Script**:
   - Execute `install.bat` to automatically download and extract dependencies (`ffmpeg`, `yt-dlp`) in bot.py folder.
   - For Linux/Mac, manually install dependencies:
     ```bash
     pip install -r requirements.txt
     sudo apt-get install ffmpeg  # or equivalent for your OS
     pip install yt-dlp
     ```

## Configuration
1. **Change `settings.cfg`**:
   First run and stop bot to create a file named `settings.cfg` in the project root, then add the following (one per line, no comments):
   ```
   YOUR_BOT_TOKEN
   PATH_TO_SAVE_FILES
   NOTIFICATIONS
   POSITIVE_REACTION
   NEGATIVE_REACTION
   ```
   - `YOUR_BOT_TOKEN`: Obtain from [BotFather](https://t.me/BotFather).
   - `PATH_TO_SAVE_FILES`: Local directory where files will be saved (e.g., `C:\Downloads` or `/home/user/downloads`).
   - `POSITIVE_REACTION`: to Emoji code
   - `POSITIVE_REACTION`: to Emoji code

2. **Create `whitelist.cfg`**:
    First run and stop bot to create a file named `whitelist.cfg` and list Telegram usernames of authorized users (one per line, no comments):
   ```
   username1
   username2
   ```

## Usage
1. **Run the Bot**:
   - On Windows, execute `run.bat`.
   - On Linux/Mac, run:
     ```bash
     python main.py
     ```

2. **Interact with the Bot**:
   - Send a photo, video, or document to the bot via Telegram.
   - Files will be downloaded to the specified `PATH_TO_SAVE_FILES/date/username/` directory.

## Directory Structure
```
FileBotTG/
├── icons/                # Contains bot logo
├── install.bat           # Installs dependencies (Windows)
├── run.bat              # Runs the bot (Windows)
├── main.py              # Main bot script
├── settings.cfg         # Configuration file
├── whitelist.cfg        # Authorized users
└── requirements.txt     # Python dependencies
```

## Notes
- Ensure `settings.cfg` and `whitelist.cfg` have no trailing spaces or comments.
- Add yourself to `whitelist.cfg` to use the bot.
- For advanced customization, review the bot's source code in `main.py`.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## About
**FileBotTG** is a private Telegram bot for secure and efficient file downloading. Built with simplicity and performance in mind, it’s perfect for personal or small-team use.

© 2025 ClosedClose
```



