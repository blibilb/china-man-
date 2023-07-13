import discord
import traceback
import psutil
import os
import urllib.request
import re
import random
import asyncio
import aiohttp

from io import BytesIO
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import errors
from util import default
from bs4 import BeautifulSoup
from asyncio import sleep
from util import lists, permissions, http, default
from discord import Webhook
from discord.ext.commands import check, CheckFailure
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        await ctx.send_help(str(ctx.invoked_subcommand))
    else:
        await ctx.send_help(str(ctx.command))

class Blacklisted(commands.CheckFailure): pass

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_join(self, guild):
        if not self.config.join_message:
            return

        try:
            to_send = sorted([chan for chan in guild.channels if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)], key=lambda x: x.position)[0]
        except IndexError:
            pass
        else:
            await to_send.send(self.config.join_message)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_command(self, ctx):
        try:
            print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")
        except AttributeError:
            print(f"Private message > {ctx.author} > {ctx.message.clean_content}")

    async def rules_reminder(self):
        await self.stdout.send("cock!")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()

        print(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)} | Members: {len(set(self.bot.get_all_members()))}')
        await self.bot.change_presence(activity=discord.Activity(name=f'{self.config.playing}', type=discord.ActivityType.streaming, url='https://www.twitch.tv/search?term=teach%20me%20english%20faggot'))

        server = self.bot.get_guild(1068933341476311150)
        channel = self.bot.get_channel(1069259149214482514)

        await channel.send(f'Ready: {self.bot.user} | Servers: {len(self.bot.guilds)} | Members: {len(set(self.bot.get_all_members()))}')

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_join(self, member):
        if "root" in member.name:
            await member.edit(nick="faggot")


async def setup(bot):
    await bot.add_cog(Events(bot))