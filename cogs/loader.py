import time
import aiohttp
import discord
import asyncio
import importlib
import os
import sys
from discord.ext.commands import has_permissions
from asyncio.subprocess import PIPE
from asyncio import sleep
from discord.ext import commands
from io import BytesIO
from util import repo, default, http, dataIO


class Loader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self._last_result = None

    @commands.command()
    @commands.check(repo.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        try:
            await self.bot.unload_extension(f"cogs.{name}")
            await self.bot.load_extension(f"cogs.{name}")
        except Exception as e: return await ctx.send(f"```\n{e}```")
        await ctx.send(f"Reloaded extension **{name}.py**")

    @commands.command()
    @commands.check(repo.is_owner)
    async def reloadall(self, ctx):
        """ Reloads all extensions. """
        error_collection = []
        for i in os.listdir("cogs"):
            if i.endswith(".py"):
                name = i[:-3]
                try: await self.bot.reload_extension(f"cogs.{name}")
                except Exception as e: error_collection.append([i, default.traceback_maker(e, advance=False)])

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(
                f"Attempted to reload all extensions, was able to reload, "
                f"however the following failed...\n\n{output}"
            )

        await ctx.send("Successfully reloaded all extensions")

    @commands.command()
    @commands.check(repo.is_owner)
    async def reloadutils(self, ctx, name: str):
        """ Reloads a utils module. """
        namemaker = f"util/{name}.py"
        try:
            module_name = importlib.import_module(f"utils.{name}")
            importlib.reload(module_name)
        except ModuleNotFoundError: return await ctx.send(f"Couldn't find module named **{namemaker}**")
        except Exception as e: return await ctx.send(f"Module **{namemaker}** returned error and was not reloaded...\n{default.traceback_maker(e)}")
        await ctx.send(f"Reloaded module **{namemaker}**")


    @commands.command()
    @has_permissions(administrator=True) 
    async def shutdown(self, ctx):
        bomb = await ctx.send(':bomb:-5:fire:')
        await asyncio.sleep(1)
        for i in range(5):
            await bomb.edit(content=f':bomb:-{4-i}:fire:')
            await asyncio.sleep(1)
        await bomb.edit(content=':boom:')
        await asyncio.sleep(1)
        await bomb.delete()
        await asyncio.sleep(1)
        await self.bot.close()
        print('Bot shutting down...')


    @commands.command()
    @commands.check(repo.is_owner)
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        try: await self.bot.load_extension(f"cogs.{name}")
        except Exception as e: return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"Loaded extension **{name}.py**")

    @commands.command()
    @commands.check(repo.is_owner)
    async def unload(self, ctx, name: str):
        """ Unload an extension. """
        try: self.bot.unload_extension(f"cogs.{name}")
        except Exception as e: return await ctx.send(f"```diff\n- {e}```")
        await ctx.send(f"Unloaded extension **{name}.py**")

async def setup(bot):
    await bot.add_cog(Loader(bot))