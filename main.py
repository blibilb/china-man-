import asyncio, os,discord,subprocess,sys,pathlib,hashlib,random
from discord.ext import commands
#from keep_alive import keep_alive
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
from util import permissions, default, repo
from util.data import Bot, HelpFormat
intents = discord.Intents.default()
intents.members = True
                                       
queues = []
blocking = False
TOKEN=token = "MTA1MDgyMTM2MDg0ODQ4NjQ1MA.GOWy_a.uJnsl94bDstwp0Skt1FAKv2wUBhZT6N4Z19ppM"
client = commands.Bot(command_prefix=';', intents=discord.Intents.all())

config = default.get("config.json")
description = """
Fuck me
"""
intents = discord.Intents.all()
print("Intents loaded")
replace_words= lambda string, dictionary: ' ' .join([dictionary[word] if word in dictionary else word for word in string.split()])

dictionary = {'i': 'ready farts'}
string = "i am ready"
print(replace_words(string, dictionary))

bot = Bot(
    command_prefix=commands.when_mentioned_or(';'),
    prefix=config.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat(),
    message_list = {},
    intents = intents
)
bot.startup = datetime.now()
async def load_cogs():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            await bot.load_extension(f"cogs.{name}")


def delete_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

@client.command()
async def bosh(ctx, images: commands.Greedy[discord.Attachment]):
    if images is None:
        await ctx.send("No images were provided.")
        return

    if not os.path.exists("gabuk"):
        os.makedirs("gabuk")

    for i, image in enumerate(images):
        if image is None:
            continue

        await image.save(f"gabuk/image{i}.jpg")
    subprocess.run(["python", "bosh.py"])
    await ctx.send('give me 10 seconds')
    await asyncio.sleep(10)
    await ctx.send(file=discord.File('gabuk/result.jpg'))
    delete_files("gabuk")

async def main():
    await load_cogs()
    await bot.start(config.token)
asyncio.run(main())

#keep_alive()
'''except Exception as e:
  if 'owner' in str(e).lower():
    os.kill(1, signal.SIGTERM)
  else:
    print(e)'''


