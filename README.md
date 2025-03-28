# Reddit Video Telegram Bot

This project monitors specific subreddits for video posts, downloads them, merges audio and video, and sends them to a Telegram channel.

## Features

- Monitors multiple subreddits for video posts.
- Downloads and merges video and audio using `yt-dlp` and `ffmpeg`.
- Prevents duplicate downloads via an SQLite database.
- Automatically sends videos to a Telegram channel using `aiogram`.

## Installation

### 1. Clone the repository

```sh
git clone https://github.com/hiisync/redtg.git
cd redtg
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Install required system dependencies

Make sure you have `yt-dlp` and `ffmpeg` installed.

#### Debian/Ubuntu

```sh
sudo apt update && sudo apt install ffmpeg
```

#### Arch Linux

```sh
sudo pacman -S ffmpeg
```

#### Windows (via Chocolatey)

```sh
choco install ffmpeg
```

### 4. Set up environment variables

Create a `.env` file in the root directory (or copy `.env.example`):

```ini
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USERNAME=your_reddit_username
PASSWORD=your_reddit_password
USER_AGENT=your_custom_user_agent

TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_telegram_channel_id
```

## Usage

### Start the bot

```sh
python src/main.py
```

The bot will start monitoring configured subreddits and send new videos to your Telegram channel.

## Project Structure

```
redtg/
│── src/
│   │── bot.py               # Telegram bot logic
│   │── config.py            # Configuration (ENV variables)
│   │── database.py          # Database operations
│   │── downloader.py        # Video downloading and processing
│   │── main.py              # Entry point
│   │── monitor.py           # Subreddit monitoring
│── requirements.txt         # Dependencies
│── .env                     # Environment variables file (ignored by Git)
```

## Contributing

Feel free to open issues or submit pull requests if you want to improve the project.

## License

This project is licensed under the MIT License.
