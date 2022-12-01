import discord
import os
import asyncio
from discord.ext import commands,tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta
import aiocron 
import time

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}({bot.user.id})')
    sign_in_reminder.start()

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


def seconds_until_7_30_AM():
    now = datetime.now()
    target = (now + timedelta(days=1)).replace(hour=12, minute=41, second=0, microsecond=0)
    diff = (target - now).total_seconds()
    print(f"{target} - {now} = {diff}")
    return diff

def seconds_until_8_30_AM():
    now = datetime.now()
    target = (now + timedelta(days=1)).replace(hour=8, minute=30, second=0, microsecond=0)
    diff = (target - now).total_seconds()
    print(f"{target} - {now} = {diff}")
    return diff

@tasks.loop(minutes=2)
async def sign_in_reminder():
    dt = datetime.now()
    targetTime = dt.ctime()
    if targetTime[11:15] == "13:0" and (dt.weekday() == 0 or dt.weekday() == 2 or dt.weekday()== 4): #mon wed fri
        print("yes!")
        channel = bot.get_channel(1047865144052555796)
        await channel.send("@everyone REMINDER TO SIGN IN")

@sign_in_reminder.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")


@tasks.loop(seconds=10)
async def sign_in_reminder_early():
    dt = datetime.now()
    targetTime = dt.ctime()
    print(dt.weekday())
    if targetTime[11:15] == "13:1" and (dt.weekday() == 1 or dt.weekday() == 3): #tues thurs
        print("yes!")
        channel = bot.get_channel(1047865144052555796)
        await channel.send("@everyone REMINDER TO SIGN IN")

@sign_in_reminder_early.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")
# bot = aBot()
sign_in_reminder.start()
if __name__ == '__main__':
    bot.run(token)


