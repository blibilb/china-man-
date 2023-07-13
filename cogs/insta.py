import json
import asyncio
import random
import discord
import json
import secrets
import asyncio
import time
import urllib.request
import re
import requests
import datetime
import aiohttp
import sqlite3
import os,instaloader, glob

from io import StringIO, BytesIO
from discord.ext import commands
from asyncio import sleep
from datetime import datetime
from util import lists, permissions, http, default
from bs4 import BeautifulSoup
from urllib.request import urlopen

from discord.ext.commands import check, CheckFailure
from discord import Webhook, utils, Embed

from PIL import Image, ImageDraw

from google_trans_new import google_translator  
from googlesearch import search as googlee

ibot = instaloader.Instaloader()
#ibot.login(user="behindthebears",passwd="nteslatesla")
import shutil

def kill(folder_path):
    try:
        shutil.rmtree(folder_path)
    except OSError as e:
        print("Error: %s : %s" % (folder_path, e.strerror))

def findmp4(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".mp4"):
                print(file)
                return file
                
    return None
def fcheck(username):
    if not os.path.exists(username):
        os.makedirs(username)
    files=glob.glob(os.path.join(username, '*'))
    try:
        [os.remove(files[i]) for i in range(len(files)) if not files[i].endswith('.mp4')]
    except:
        pass

async def downloadPost(files,username, count):
        kill(username)
        try:
            profile = instaloader.Profile.from_username(ibot.context, username)
            c=0
            posts = profile.get_posts()
            for index, post in enumerate(posts, 1):
                if c < count:
                    print(post.url)
                    ibot.download_post(post, target=f"{profile.username}")
                    c+=1
                else:
                    break
            fcheck(username)
            return True
        except Exception as e:
            print(e)
            return False
        

    
class insta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.session = aiohttp.ClientSession()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['ig','gram'])
    async def insta(self,ctx,username, count: int= 1):
        """instagram poster"""
        if count>10:
            ctx.send('no more than 10 posts, reducing it to 10.')
            count=10
        async with ctx.channel.typing():
            messagewdwdad = await ctx.send("Working... *VROOOM*")
            print(username)
            files=glob.glob(os.path.join(username, '*'))
            if await downloadPost(files,username,count):
                print('true!')
                
                await ctx.send(files=[discord.File(f"{username}/{name}") for i, name in enumerate(os.listdir(username)) if i<10])
        await messagewdwdad.delete()
'''    async def insta2(self,ctx,username, count: int= 1):
        """instagram poster"""
        if count>10:
            ctx.send('no more than 10 posts, reducing it to 10.')
            count=10
        async with ctx.channel.typing():
            messagewdwdad = await ctx.send("Working... *VROOOM*")
            print(username)
            files=glob.glob(os.path.join(username, '*'))
            if await downloadPost(files,username,count):
                print('true!')
                fcheck(username)
                await ctx.send(files=[discord.File(f"{username}/{name}") for i, name in enumerate(os.listdir(username)) if i<10])
        await messagewdwdad.delete()'''


async def setup(bot):
    await bot.add_cog(insta(bot))