import sqlite3
from config import DB_FILE

def init_db():
    """Creates the database table if it does not exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS downloaded_posts (post_id TEXT PRIMARY KEY)")
        conn.commit()

def is_post_downloaded(post_id: str) -> bool:
    """Checks if a post has already been downloaded."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM downloaded_posts WHERE post_id = ?", (post_id,))
        return cursor.fetchone() is not None

def add_downloaded_post(post_id: str):
    """Adds a post ID to the database to prevent duplicate downloads."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO downloaded_posts (post_id) VALUES (?)", (post_id,))
        conn.commit()
