from discord.ext import tasks
import datetime
from client import client
from api import get_daily_challenge, get_upcoming_contests
from config import CHANNEL_IDS, LOCAL_TZ


@tasks.loop(time=datetime.time(hour=0, minute=0, second=30))
async def post_daily_challenge_thread():
    print("Posting daily challenge thread...")
    # Get daily challenge
    daily_challenge = get_daily_challenge()
    # Create thread
    channel = client.get_channel(CHANNEL_IDS["DAILY_CHALLENGE"])
    message = await channel.send(
        f"# 🔥 {daily_challenge["date"]}: LeetCode Daily Challenge\n## [{daily_challenge["question"]["frontendQuestionId"]}. {daily_challenge["question"]["title"]}](https://leetcode.com/problems/{daily_challenge["question"]["titleSlug"]}/description/?envType=daily-question&envId={daily_challenge["date"]})"
    )
    thread = await message.create_thread(name=f"🔥 {daily_challenge["date"]}")
    await thread.send(content="Discuss today's problem here 🧵")
    print("Posted daily challenge thread.")
    return None
