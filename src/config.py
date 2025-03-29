import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
PASSWORD = os.getenv("PASSWORD")
USERNAME = os.getenv("USERNAME")
USER_AGENT = os.getenv("USER_AGENT")

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

DB_FILE = "downloaded_posts.db"
SUBREDDITS_TO_MONITOR = ["funny", "memes", "FunnyAnimals", "funnyvideos", "MadeMeSmile", "oddlysatisfying", "HumansBeingBros", "nextfuckinglevel"]
