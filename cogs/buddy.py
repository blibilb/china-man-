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

class buddy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.session = aiohttp.ClientSession()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['9x'])
    async def buddy(self,ctx,link: str):
        """gives a video from any link (work in progress)"""
        url=f'https://9xbuddy.xyz/process?url={link}'
        response = requests.get(url)
        await asyncio.sleep(4)
        print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        x= await ctx.send('here:\n')
        for a in soup.find_all('a', href=True):
            x= await x.edit(content=x.content+'\n'+str(a['href']))
            print ("Found the URL:", a['href'])
        
        
async def setup(bot):
    await bot.add_cog(buddy(bot))