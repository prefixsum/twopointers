import disnake
import os
import logging
from disnake.ext import commands
import tasks
from config_manager import ensure_config_directory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

intents = disnake.Intents.default()
intents.messages = True

bot = commands.InteractionBot(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    tasks.daily_problem.start()
    tasks.weekly_contest.start()
    tasks.biweekly_contest.start()


tasks.set_bot_reference(bot)
tasks.set_logger(logger)

bot.load_extension("commands")


ensure_config_directory()

TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
bot.run(TOKEN)
