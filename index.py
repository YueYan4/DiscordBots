from multiprocessing.connection import answer_challenge
from click import pass_context
import discord
import os, sys
import time, datetime, sched
from threading import Thread
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from dotenv import load_dotenv
from keep_alive import keep_alive
import pytz, pytest
from datetime import datetime

bot = commands.Bot(command_prefix="$")

scheduler = AsyncIOScheduler(timezone="US/Eastern")

#Next, we create an instance of a Client. This is the connection to Discord.
#client = discord.Client()


#The @client.event() decorator is used to register an event. This is an asynchronous library, so things are done with callbacks. A callback is a function that is called when something else happens. In this code, the on_ready() event is called when the bot is ready to start being used. Then, when the bot receives a message, the on_message() event is called.
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
# def __init__(self):
#     self.client = discord.Client()
#     self.on_ready = self.client.event(self.on_ready)
#     self.on_message = self.client.event(self.on_message)

def send(message):
    message.channel.send('Stamina is full')


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


async def send_new(ctx, msg, t=True):
    await ctx.send(msg)
    t = False


@bot.command()
async def new(ctx, msg, hr=None, mi=None, month=None, day=None):
    if msg == None:
        ctx.send("No message")
        return
    if hr == None:
        hr = datetime.now().hr
    if mi == None:
        mi = datetime.now().minute
    if month == None:
        month = datetime.now().month
    if day == None:
        day = datetime.now().day
    await ctx.send("Ok! At {}:{} on {}/{} I'll send the msg \"{}\".".format(hr, mi, month, day, msg))
    scheduler = AsyncIOScheduler(timezone="US/Eastern")
    scheduler.add_job(send_new,
                      CronTrigger(month=month,
                                  day=day,
                                  hour=hr,
                                  minute=mi,
                                  second="0",
                                  timezone='US/Eastern'),
                      args=(ctx, msg))
    scheduler.start()



#The on_message() event triggers each time a message is received but we don't want it to do anything if the message is from ourselves. So if the Message.author is the same as the Client.user the code just returns.


@bot.event  #print that the bot is ready to make sure that it actually logged on
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.event
async def on_message(message):
    if str(message.content).lower().startswith("help"):
        await message.channel.send(
            'NOTIFICATIONS:\n$sekai\n$resin\n$realm\n$new "msg" hour minute month (optional) day (optional)\nType $time to get all timer(s)\nType $time [timer name] to get the timer\nType $stop [timer name] to stop timers\nType "get timer names"\nType $stop all to stop all timers\n$exit'
        )


#Next, we check if the Message.content starts with '$hello'. If so, then the bot replies with 'Hello!' to the channel it was used in.        
        
    if str(message.content).lower() == ("$exit"):
        await message.channel.send("Bye-Bye!!")
        exit(0)
    if str(message.content).lower() == ("$stop all"):
        await message.channel.send("Getting rid of all timers")
        restart_bot()
    if str(message.content).lower() == "get timer names":
      await message.channel.send("\nresin\nsekai\nentrust\nrealm")
    await bot.process_commands(message)


sekai_on = False
sekai_time = False
sekai_arr = []
sekai_job_id = None
@bot.command()
async def sekai(ctx):
  global sekai_on, sekai_arr, sekai_time, sekai_job_id, scheduler
  if sekai_on:
    sekai_job_id.remove()
    return
  if sekai_on == False:
    await ctx.send("Ok, going!")
    sekai_time = True
    ti = datetime.now(pytz.timezone('US/Eastern')) + timedelta(hours = 5)
    hr = ti.hour
    min = ti.minute
    sec = ti.second
    sekai_arr.append(hr)
    sekai_arr.append(min)
    sekai_arr.append(sec)
    sekai_job_id = scheduler.add_job(send_new,
                        CronTrigger(hour=hr, minute = min,
                                    second=sec,
                                    timezone='US/Eastern'),
                        args=(ctx, "Stamina is full!", sekai_time))
    scheduler.start()

realm_on = False
realm_time = False
realm_arr = []
realm_job_id = None
@bot.command()
async def entrust(ctx):
  global realm_on, realm_arr, realm_time, realm_job_id, scheduler
  if realm_on:
    realm_job_id.remove()
    return
  if realm_on == False:
    await ctx.send("Ok, going!")
    realm_time = True
    ti = datetime.now(pytz.timezone('US/Eastern')) + timedelta(hours = 6)
    hr = ti.hour
    min = ti.minute
    sec = ti.second
    realm_arr.append(hr)
    realm_arr.append(min)
    realm_arr.append(sec)
    realm_job_id = scheduler.add_job(send_new,
                        CronTrigger(hour=hr, minute = min,
                                    second=sec,
                                    timezone='US/Eastern'),
                        args=(ctx, "Entrusted realm is done!", realm_time))
    scheduler.start()

@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

@bot.command()
async def stop(ctx, name):
  global sekai_on, sekai_time, sekai_arr, sekai_job_id
  global resin_on, resin_time, resin_arr, resin_job_id
  if name.lower() == "sekai":
    await ctx.send("Sekai timer has stopped")
    sekai_on = True
    await sekai(ctx)
    sekai_on = False
    sekai_time = False
    sekai_arr.clear()
    sekai_job_id = None
    
  if name.lower() == "resin":
    await ctx.send("Resin timer has stopped")
    resin_on = True
    await resin(ctx)
    resin_on = False
    resin_time = False
    resin_arr.clear()
    resin_job_id = None

  if name.lower() == "entrust":
    await ctx.send("Entrusted realm timer has stopped")
    realm_on = True
    await entrust(ctx)
    realm_on = False
    realm_time = False
    realm_arr.clear()
    realm_job_id = None
    
  if name.lower() == "realm":
    await ctx.send("My realm timer has stopped")
    r_on = True
    await realm(ctx)
    r_on = False
    r_time = False
    r_arr.clear()
    r_job_id = None
  
resin_on = False
resin_time = False
resin_arr = []
resin_job_id = None
@bot.command()
async def resin(ctx):
    global resin_on, resin_time, resin_arr, scheduler, resin_job_id
    if resin_on:
      resin_job_id.remove()
      return
    await ctx.send("How much resin do you have?")

    def check(message):
        return message.author == ctx.author

    resin = (160 - int(
        (await bot.wait_for("message", check=check)).content)) * 8
    cur = datetime.now(pytz.timezone('US/Eastern')) + timedelta(minutes=resin)
    cur = cur.replace(microsecond=0)
    form = cur.time().strftime('%H:%M')
    await ctx.send("Resin will replenish at " + form)
    time.sleep(1)

    def check2(message):
        return message.author == ctx.author

    await ctx.send("Remind when full?")
    ans = await bot.wait_for("message", check=check2)
    ans = ans.content
    hr = int(cur.hour)
    min = int(cur.minute)
    sec = int(cur.second)
    resin_arr.append(hr)
    resin_arr.append(min)
    resin_arr.append(sec)
    if str(ans).lower() == "yes" or str(ans).lower() == "y":
          resin_time = True
          await ctx.send("Ok, I'll remind you")
          resin_job_id = scheduler.add_job(send_new,
                        CronTrigger(hour=hr, minute = min,
                                    second=sec,
                                    timezone='US/Eastern'),
                        args=(ctx, "Resin is full!", resin_time))
          scheduler.start()
        
r_on = False
r_time = False
r_arr = []
r_job_id = None
@bot.command()
async def realm(ctx, h=0, m=0):
    global r_on, r_time, r_arr, scheduler, r_job_id
    if r_on:
      r_job_id.remove()
      return

    cur = datetime.now(pytz.timezone('US/Eastern')) + timedelta(hours=int(h), minutes=int(m))
    cur = cur.replace(microsecond=0)
    form = cur.time().strftime('%H:%M')
    await ctx.send("Realm expires at " + form + ". I'll remind you!")
    hr = int(cur.hour)
    min = int(cur.minute)
    sec = int(cur.second)
    r_arr.append(hr)
    r_arr.append(min)
    r_arr.append(sec)
    
    r_time = True
    r_job_id = scheduler.add_job(send_new,
                        CronTrigger(hour=hr, minute = min,
                                    second=sec,
                                    timezone='US/Eastern'),
                        args=(ctx, "My realm is expired!", r_time))
    scheduler.start()
    r_time = False
  
def t(hours, mins, secs):
  now = datetime.now(pytz.timezone('US/Eastern'))
  now_hour = now.hour
  now_min = now.minute
  now_sec = now.second
  if hours < now_hour:
    hours = hours + 24
  start = timedelta(hours = now_hour, minutes = now_min, seconds = now_sec)
  end = timedelta(hours=hours, minutes = mins, seconds = secs)
  total = end - start
  sc = int(total.total_seconds())
  mn, sc = divmod(sc, 60) 
  hr, mn = divmod(mn, 60)
  timer = '{:02d}:{:02d}:{:02d}'.format(hr, mn, sc)
  return timer

@bot.command()
async def timer(ctx, name="None"):
  global sekai_time, resin_time, sekai_arr, resin_arr, realm_time, realm_arr, r_time, r_arr
  if name == "None":
    if sekai_time:
      await ctx.send("Sekai: " + t(sekai_arr[0], sekai_arr[1], sekai_arr[2]))
    if resin_time:
      await ctx.send("Resin: " + t(resin_arr[0], resin_arr[1], resin_arr[2]))
    if realm_time:
      await ctx.send("Entrusted Realm: " + t(realm_arr[0], realm_arr[1], realm_arr[2]))
    if r_time:
      await ctx.send("My Realm: " + t(r_arr[0], r_arr[1], r_arr[2]))
    if sekai_time == False and resin_time == False and realm_time == False and r_time == False:
      await ctx.send("No timers running")
  if name.lower() == "sekai":
    if sekai_time:
      await ctx.send("Sekai: " + t(sekai_arr[0], sekai_arr[1], sekai_arr[2]))
  if name.lower() == "resin":
    if resin_time:
      await ctx.send("Resin: " + t(resin_arr[0], resin_arr[1], resin_arr[2]))
  if name.lower() == "entrust":
    if realm_time:
      await ctx.send("Entrusted Realm: " + t(realm_arr[0], realm_arr[1], realm_arr[2]))
  if name.lower() == "realm":
    if r_time:
      await ctx.send("My Realm: " + t(r_arr[0], r_arr[1], r_arr[2]))
  


TOKEN = os.getenv('NOTIF')

try:
  keep_alive()
  bot.run(TOKEN)
except discord.errors.HTTPException as err:
  if err.code == 429:
    os.system('kill 1')