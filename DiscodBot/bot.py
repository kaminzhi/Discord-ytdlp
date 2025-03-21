import discord
from discord.ext import commands
import config
import os

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and file != "__init__.py":
            await bot.load_extension(f"cogs.{file[:-3]}")  # 去掉 .py 副檔名


@bot.event
async def on_ready():
    print(f"✅ 已啟動 {bot.user}")
    await load_cogs()


bot.run(config.TOKEN)

