import discord
import os, sys
import time, datetime, sched
from threading import Thread
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

bot = commands.Bot(command_prefix="/")
TOKEN = os.getenv('TOKEN')


async def func1():
    await bot.wait_until_ready()
    channel = bot.get_channel(997185227757727757)
    await channel.send("GB NOW!")


async def func2():
    await bot.wait_until_ready()
    channel = bot.get_channel(997185227757727757)
    await channel.send("GB in 2 mins!")


async def func3():
    await bot.wait_until_ready()
    channel = bot.get_channel(997185227757727757)
    await channel.send("GB in 1 mins!")


async def func4():
    await bot.wait_until_ready()
    channel = bot.get_channel(997185227757727757)
    await channel.send("Take the pill!")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    #initializing scheduler
    scheduler = AsyncIOScheduler(timezone="US/Eastern")
    #sends "Your Message" at 12PM and 18PM (Local Time)
    scheduler.add_job(
        func1,
        CronTrigger(hour="14, 19",
                    minute="0",
                    second="0",
                    timezone='US/Eastern'))
    scheduler.add_job(
        func2,
        CronTrigger(hour="13, 18",
                    minute="58",
                    second="0",
                    timezone='US/Eastern'))
    scheduler.add_job(
        func3,
        CronTrigger(hour="13, 18",
                    minute="59",
                    second="0",
                    timezone='US/Eastern'))
    scheduler.add_job(
        func4,
        CronTrigger(hour="18", minute="0", second="0", timezone='US/Eastern'))
    #starting the scheduler
    scheduler.start()

TOKEN = os.getenv('GB')
try:
  keep_alive()
  bot.run(TOKEN)
except discord.errors.HTTPException as err:
  os.system('kill 1')
