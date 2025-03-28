import os
import subprocess
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from bot import bot
from database import add_downloaded_post, is_post_downloaded
from config import CHANNEL_ID

async def download_and_send_video(post):
    """Downloads video, merges audio & video, and sends it to a Telegram channel."""
    if is_post_downloaded(post.id):
        return

    print(f"📌 New video: {post.title}")

    reddit_url = f"https://www.reddit.com{post.permalink}"
    video_output = f"{post.id}_video.mp4"
    audio_output = f"{post.id}_audio.mp4"
    final_output = f"{post.id}.mp4"

    try:
        subprocess.run(["yt-dlp", "-f", "bv", reddit_url, "-o", video_output], check=True)
        subprocess.run(["yt-dlp", "-f", "ba", reddit_url, "-o", audio_output], check=True)
        subprocess.run([
            "ffmpeg", "-y", "-i", video_output, "-i", audio_output,
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", final_output
        ], check=True)

        print(f"✅ Downloaded: {final_output}")
        add_downloaded_post(post.id)

        video_file = FSInputFile(final_output)
        caption = f"{post.title}\n\n[r/{post.subreddit.display_name}]({post.url})"
        await bot.send_video(CHANNEL_ID, video=video_file, caption=caption, parse_mode=ParseMode.MARKDOWN)

        os.remove(video_output)
        os.remove(audio_output)
        os.remove(final_output)

    except subprocess.CalledProcessError as e:
        print(f"❌ Download error: {e}")
