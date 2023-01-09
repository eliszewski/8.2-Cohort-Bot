import discord
import os
import asyncio
from discord.ext import commands,tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}({bot.user.id})')
    while True:
        await send_message_on_schedule()
        await asyncio.sleep(60)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(message):
    if message.content == 'small':
        await message.channel.send("<@1034085613902757928>")
    
async def send_message_on_schedule():
    message = "@everyone SIGN IN"
    today = datetime.today().weekday()
    if today == 1 or today == 3:
        now = datetime.now()
        if now.hour == 7 and now.minute == 15:
            text_channel = bot.get_channel(1047865144052555796)
            await text_channel.send(message)
    if today == 0 or today == 2  or today == 4:
        now = datetime.now()
        if now.hour == 8 and now.minute == 15:
            text_channel = bot.get_channel(1047865144052555796)
            await text_channel.send(message)

if __name__ == '__main__':
    bot.run(token)


