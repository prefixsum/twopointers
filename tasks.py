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


@tasks.loop(time=datetime.time(hour=1, minute=30, second=30))
async def post_weekly_contest_thread():
    print("Checking for weekly contest...")
    # Get next weekly contest
    upcoming_contests = get_upcoming_contests()
    contest = (
        upcoming_contests[0]
        if "biweekly" not in upcoming_contests[0]["titleSlug"]
        else upcoming_contests[1]
    )
    # Check time until contest
    current_time = datetime.datetime.now()
    contest_start_time = datetime.datetime.fromtimestamp(contest["startTime"])
    if contest_start_time - current_time > datetime.timedelta(hours=6):
        print("No weekly contest today.")
        return None
    # Create thread
    channel = client.get_channel(CHANNEL_IDS["WEEKLY_CONTEST"])
    message = await channel.send(
        f"# 🏆 [{contest["title"]}](https://leetcode.com/contest/{contest["titleSlug"]})"
    )
    thread = await message.create_thread(name=f"🏆 {contest["title"]}")
    await thread.send(
        content=f"{contest["title"]} starts in 1 hour. Discuss the contest here 🧵\n\n⚠️🚨 *Do not disclose solutions before the end of the contest!*"
    )
    print("Posted weekly contest thread.")
    return None


@tasks.loop(time=datetime.time(hour=13, minute=30, second=30))
async def post_biweekly_contest_thread():
    print("Checking for biweekly contest...")
    # Get next biweekly contest
    upcoming_contests = get_upcoming_contests()
    contest = (
        upcoming_contests[0]
        if "biweekly" in upcoming_contests[0]["titleSlug"]
        else upcoming_contests[1]
    )
    # Check time until contest
    current_time = datetime.datetime.now()
    contest_start_time = datetime.datetime.fromtimestamp(contest["startTime"])
    if contest_start_time - current_time > datetime.timedelta(hours=6):
        print("No biweekly contest today.")
        return None
    # Create thread
    channel = client.get_channel(CHANNEL_IDS["WEEKLY_CONTEST"])
    message = await channel.send(
        f"# 🏆 [{contest["title"]}](https://leetcode.com/contest/{contest["titleSlug"]})"
    )
    thread = await message.create_thread(name=f"🏆 {contest["title"]}")
    await thread.send(
        content=f"{contest["title"]} starts in 1 hour. Discuss the contest here 🧵\n\n⚠️🚨 *Do not disclose solutions before the end of the contest!*"
    )
    print("Posted biweekly contest thread.")
    return None
