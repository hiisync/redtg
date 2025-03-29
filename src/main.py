import asyncio
from asyncpraw import Reddit
from config import CLIENT_ID, CLIENT_SECRET, PASSWORD, USER_AGENT, USERNAME, SUBREDDITS_TO_MONITOR
from database import init_db
from monitor import monitor_subreddit

async def main():
    """Main asynchronous function to initialize Reddit and start monitoring subreddits."""
    async with Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME,
    ) as reddit:
        # Create a task for each subreddit to monitor
        tasks = [monitor_subreddit(reddit, subreddit_name) for subreddit_name in SUBREDDITS_TO_MONITOR]
        # Run all tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Initialize the database before starting
    init_db()
    # Run the main async function
    asyncio.run(main())
