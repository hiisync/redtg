import asyncio
from asyncpraw import Reddit
from config import CLIENT_ID, CLIENT_SECRET, PASSWORD, USER_AGENT, USERNAME, SUBREDDITS_TO_MONITOR
from downloader import download_and_send_video
from database import is_post_downloaded

async def process_submission(submission):
    """Processes a new video post."""
    if submission.is_video and not is_post_downloaded(submission.id):
        await download_and_send_video(submission)

async def monitor_subreddit(reddit, subreddit_name):
    """Monitors a specific subreddit and processes new video posts."""
    try:
        subreddit = await reddit.subreddit(subreddit_name)
        async for submission in subreddit.stream.submissions():
            await process_submission(submission)
    except Exception as e:
        print(f"⚠️ Error in subreddit {subreddit_name}: {e}")
        await asyncio.sleep(10)  # Pause before retrying
