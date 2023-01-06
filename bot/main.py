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
    while True:
        # call the send_message_on_schedule function
        await send_message_on_schedule()
        # wait for one minute before checking again
        await asyncio.sleep(60)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(message):
    if message.content == 'small':
        await message.channel.send("<@1034085613902757928>")
    

def getTime():
    return datetime.now()
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
    await asyncio.sleep(2)
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
    dt = getTime
    targetTime = dt.ctime()
    print(dt.weekday())
    await asyncio.sleep(2)
    if targetTime[11:15] == "13:3" and (dt.weekday() == 1 or dt.weekday() == 3): #tues thurs
        print("yes!")
        channel = bot.get_channel(1047865144052555796)
        await channel.send("@everyone REMINDER TO SIGN IN")

@sign_in_reminder_early.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")
# bot = aBot()

async def send_message_on_schedule():
    message = "@everyone SIGN IN"
    # get the current day of the week
    today = datetime.today().weekday()
    # if today is Tuesday or Thursday
    if today == 1 or today == 3:
        # get the current time
        now = datetime.now()
        # if the current time is 7:15 am
        if now.hour == 7 and now.minute == 15:
            # get the text channel that the message will be sent to
            text_channel = bot.get_channel()
            # create the message
            # send the message
            await text_channel.send(message)
    if today == 0 or today == 2  or today == 4:
        now = datetime.now()
        # if the current time is 7:15 am
        if now.hour == 8 and now.minute == 15:
            # get the text channel that the message will be sent to
            text_channel = bot.get_channel(1047865144052555796)
            # create the message
            # send the message
            await text_channel.send(message)

if __name__ == '__main__':
    bot.run(token)


