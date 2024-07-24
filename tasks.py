# tasks.py
import datetime
import os
import disnake
import api
import logging
from disnake.ext import tasks
from config_manager import load_config

bot = None
logger = None


def set_bot_reference(bot_reference):
    global bot
    bot = bot_reference


def set_logger(logger_reference):
    global logger
    logger = logger_reference


@tasks.loop(time=datetime.time(hour=0, minute=0, second=30))
async def daily_problem():
    logger.info("Posting daily challenge thread...")

    daily_challenge = api.get_daily_challenge()

    for filename in os.listdir("server_configs"):
        guild_id = filename.split(".")[0]
        config = load_config(guild_id)

        if "daily_problem" in config and config["daily_problem"]["enabled"]:
            channel_id = config["daily_problem"]["channel_id"]
            channel = bot.get_channel(channel_id)

            if channel:
                try:
                    message_text = (
                        f"# 🔥 {daily_challenge['date']}: LeetCode Daily Challenge\n"
                        f"## [{daily_challenge['question']['frontendQuestionId']}. {daily_challenge['question']['title']}]"
                        f"(https://leetcode.com/problems/{daily_challenge['question']['titleSlug']}/description/?envType=daily-question&envId={daily_challenge['date']})"
                    )
                    message = await channel.send(message_text)
                    thread_name = f"🔥 {daily_challenge['date']}"
                    thread = await message.create_thread(name=thread_name)
                    await thread.send(content="Discuss today's problem here 🧵")
                    logger.info(f"Posted daily challenge thread in {channel.name}.")
                except disnake.HTTPException as e:
                    logger.info(f"Failed to post in {channel.name}: {str(e)}")
            else:
                logger.info(
                    f"No valid channel configured for daily challenges in guild {guild_id}."
                )
        else:
            logger.info(
                f"No configuration for daily challenges or it is disabled in guild {guild_id}."
            )


@tasks.loop(time=datetime.time(hour=1, minute=30, second=30))
async def weekly_contest():
    logger.info("Checking for weekly contest...")

    upcoming_contests = api.get_upcoming_contests()
    contest = (
        upcoming_contests[0]
        if "biweekly" not in upcoming_contests[0]["titleSlug"]
        else upcoming_contests[1]
    )

    current_time = datetime.datetime.now()
    contest_start_time = datetime.datetime.fromtimestamp(contest["startTime"])
    if contest_start_time - current_time > datetime.timedelta(hours=8):
        logger.info("No weekly contest today.")
        return

    for filename in os.listdir("server_configs"):
        guild_id = filename.split(".")[0]
        config = load_config(guild_id)

        if "weekly_contest" in config and config["weekly_contest"]["enabled"]:
            channel_id = config["weekly_contest"]["channel_id"]
            channel = bot.get_channel(channel_id)

            if channel:
                try:
                    message_text = f"# 🏆 [{contest['title']}](https://leetcode.com/contest/{contest['titleSlug']})"
                    message = await channel.send(message_text)
                    thread_name = f"🏆 {contest['title']}"
                    thread = await message.create_thread(name=thread_name)
                    await thread.send(
                        content=f"{contest['title']} starts in 1 hour. Discuss the contest here 🧵\n\n⚠️🚨 *Do not disclose solutions before the end of the contest!*"
                    )
                    logger.info(f"Posted weekly contest thread in {channel.name}.")
                except disnake.HTTPException as e:
                    logger.info(f"Failed to post in {channel.name}: {str(e)}")
            else:
                logger.info(
                    f"No valid channel configured for weekly contests in guild {guild_id}."
                )
        else:
            logger.info(
                f"No configuration for weekly contests or it is disabled in guild {guild_id}."
            )


@tasks.loop(time=datetime.time(hour=13, minute=30, second=30))
async def biweekly_contest():
    logger.info("Checking for biweekly contest...")

    upcoming_contests = api.get_upcoming_contests()
    contest = (
        upcoming_contests[0]
        if "biweekly" in upcoming_contests[0]["titleSlug"]
        else upcoming_contests[1]
    )

    current_time = datetime.datetime.now()
    contest_start_time = datetime.datetime.fromtimestamp(contest["startTime"])
    if contest_start_time - current_time > datetime.timedelta(hours=8):
        logger.info("No biweekly contest today.")
        return

    for filename in os.listdir("server_configs"):
        guild_id = filename.split(".")[0]
        config = load_config(guild_id)

        if "biweekly_contest" in config and config["biweekly_contest"]["enabled"]:
            channel_id = config["biweekly_contest"]["channel_id"]
            channel = bot.get_channel(channel_id)

            if channel:
                try:
                    message_text = f"# 🏆 [{contest['title']}](https://leetcode.com/contest/{contest['titleSlug']})"
                    message = await channel.send(message_text)
                    thread_name = f"🏆 {contest['title']}"
                    thread = await message.create_thread(name=thread_name)
                    await thread.send(
                        content=f"{contest['title']} starts in 1 hour. Discuss the contest here 🧵\n\n⚠️🚨 *Do not disclose solutions before the end of the contest!*"
                    )
                    logger.info(f"Posted biweekly contest thread in {channel.name}.")
                except disnake.HTTPException as e:
                    logger.info(f"Failed to post in {channel.name}: {str(e)}")
            else:
                logger.info(
                    f"No valid channel configured for biweekly contests in guild {guild_id}."
                )
        else:
            logger.info(
                f"No configuration for biweekly contests or it is disabled in guild {guild_id}."
            )


async def before_tasks():
    await bot.wait_until_ready()
