import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from discord import Activity, ActivityType

##############################################################################################

load_dotenv()
bot_secret = os.getenv('BOT_SECRET')

##############################################################################################

# discord setup


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def startup(self):
        await bot.wait_until_ready()

        # If you want to define specific guilds, pass a discord object with id (Currently, this is global)
        await bot.tree.sync()
        print('Sucessfully synced applications commands')
        print(f'Connected as {bot.user}')
        await bot.change_presence(activity=discord.Game(name=""))

    async def setup_hook(self):
        for root, dirs, files in os.walk("./cogs"):
            for filename in files:
                if filename.endswith(".py"):
                    try:
                        await bot.load_extension(root[2:].replace("/", ".") + "." + filename[:-3])
                        print(f"Loaded {filename}")
                    except Exception as e:
                        print(f"Failed to load {filename}")
                        print(f"[ERROR] {e}")

        self.loop.create_task(self.startup())


bot = Bot()
bot.run(bot_secret)
