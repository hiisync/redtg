import asyncio
from database import init_db
from monitor import monitor_subreddits

if __name__ == "__main__":
    init_db()
    asyncio.run(monitor_subreddits())
