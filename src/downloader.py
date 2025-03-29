import asyncio
import os
import subprocess
import time
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from bot import bot
from database import add_downloaded_post, is_post_downloaded
from config import CHANNEL_ID

async def download_video(reddit_url, video_output):
    """Download video."""
    process = subprocess.run(["yt-dlp", "-f", "bv", reddit_url, "-o", video_output])
    if process.returncode != 0:
        print(f"❌ Video download failed: {process.returncode}")
        return False
    return True

async def download_audio(reddit_url, audio_output):
    """Download audio."""
    process = subprocess.run(["yt-dlp", "-f", "ba", reddit_url, "-o", audio_output])
    if process.returncode != 0:
        print(f"❌ Audio download failed: {process.returncode}")
        return False
    return True

async def merge_video_and_audio(video_output, audio_output, final_output):
    """Merge video and audio files."""
    process = subprocess.run([
        "ffmpeg", "-y", "-i", video_output, "-i", audio_output,
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", final_output
    ])
    if process.returncode != 0:
        print(f"❌ FFmpeg merge failed: {process.returncode}")
        return False
    return True

async def handle_429_error():
    """Handle 429 errors by waiting before retrying."""
    print("❌ Too many requests. Retrying after a delay.")
    await asyncio.sleep(60)

async def download_and_send_video(post):
    """Main function to download and send video."""
    if is_post_downloaded(post.id):
        return

    print(f"📌 New video: {post.title}")

    reddit_url = f"https://www.reddit.com{post.permalink}"
    video_output = f"videos/{post.id}_video.mp4"
    audio_output = f"videos/{post.id}_audio.mp4"
    final_output = f"videos/{post.id}.mp4"

    try:
        # Attempt to download video and audio
        if not await download_video(reddit_url, video_output):
            return  # Skip if video download fails

        if not await download_audio(reddit_url, audio_output):
            return  # Skip if audio download fails

        # Attempt to merge video and audio
        if not await merge_video_and_audio(video_output, audio_output, final_output):
            return  # Skip if merge fails

        print(f"✅ Downloaded: {final_output}")
        add_downloaded_post(post.id)

        video_file = FSInputFile(final_output)
        caption = f"{post.title}\n\n[r/{post.subreddit.display_name}]({post.url})"
        await bot.send_video(CHANNEL_ID, video=video_file, caption=caption, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(300)  # Sleep to avoid hitting the rate limit

        # Clean up the files after sending
        os.remove(video_output)
        os.remove(audio_output)
        os.remove(final_output)

    except subprocess.CalledProcessError as e:
        print(f"❌ Download error: {e}")
    except Exception as e:
        # Handle 429 error
        if "HTTP Error 429" in str(e):
            await handle_429_error()
            await download_and_send_video(post)  # Retry the same post after waiting
        else:
            print(f"❌ Unexpected error: {e}")
