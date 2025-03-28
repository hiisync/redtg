import asyncio
from asyncpraw import Reddit
from config import CLIENT_ID, CLIENT_SECRET, PASSWORD, USER_AGENT, USERNAME, SUBREDDITS_TO_MONITOR
from downloader import download_and_send_video
from database import is_post_downloaded

async def monitor_subreddits():
    """Monitors subreddits and processes new video posts."""
    async with Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME,
    ) as reddit:
        while True:
            try:
                for subreddit_name in SUBREDDITS_TO_MONITOR:
                    subreddit = await reddit.subreddit(subreddit_name)
                    async for post in subreddit.hot(limit=10):
                        if post.is_video and not is_post_downloaded(post.id):
                            await download_and_send_video(post)
                
                # Add a delay before the next iteration
                await asyncio.sleep(5) 

            except Exception as e:
                print(f"⚠️ Error: {e}")
                await asyncio.sleep(10)
