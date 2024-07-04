import os
from client import client
from tasks import (
    post_daily_challenge_thread,
    post_weekly_contest_thread,
    post_biweekly_contest_thread,
)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    post_daily_challenge_thread.start()
    post_weekly_contest_thread.start()
    post_biweekly_contest_thread.start()


# Run the bot
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
client.run(TOKEN)
