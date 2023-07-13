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
import os
import openai,praw,asyncpraw
reddit = asyncpraw.Reddit(client_id='3TTxM-vWr7BJAYmo4iIG8w',
                     client_secret='tacBznSDMSAprY4ovYriDyU2-0CWnA',
                     user_agent='china man')
openai.api_key = "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"
from io import StringIO, BytesIO
from discord.ext import commands
from asyncio import sleep
from datetime import datetime
from util import lists, permissions, http, default
from bs4 import BeautifulSoup
from urllib.request import urlopen

from discord.ext.commands import check, CheckFailure,has_permissions
from discord import Webhook, utils, Embed

from PIL import Image, ImageDraw
import io
from google_trans_new import google_translator  
from googlesearch import search as googlee

import requests
import json
import time
import replicate
os.environ["REPLICATE_API_TOKEN"] = 'cda13507234110706eed5d61378e1790df9819e0'
replicate.Client(api_token=["REPLICATE_API_TOKEN"])
model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get("f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1")

# https://replicate.com/stability-ai/stable-diffusion/versions/f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1#input

message_list = {}
BASE_URL = "https://api.luan.tools/api/tasks/"
HEADERS = {
    'Authorization': 'bearer oZFb5vfcICAbdga7mP05lg0vPogYHbGZ',
    'Content-Type': 'application/json'
}

path=None
def send_task_to_dream_api(prompt, style_id=3, target_img_path=None):
    """
    Send requests to the dream API.
    prompt is the text prompt.
    style_id is which style to use (a mapping of ids to names is in the docs).
    target_img_path is an optional path to an image to influence the generation.
    """

    # Step 1) make a POST request to https://api.luan.tools/api/tasks/
    post_payload = json.dumps({
        path: bool(target_img_path)
    })
    post_response = requests.request(
        "POST", BASE_URL, headers=HEADERS, data=post_payload)
    
    # Step 2) skip this step if you're not sending a target image otherwise,
    # upload the target image to the url provided in the response from the previous POST request.
    if target_img_path:
        target_image_url = post_response.json()["target_image_url"]
        with open(target_img_path, 'rb') as f:
            fields = target_image_url["fields"]
            fields ["file"] = f.read()
            requests.request("POST", url=target_image_url["url"], files=fields)

    # Step 3) make a PUT request to https://api.luan.tools/api/tasks/{task_id}
    # where task id is provided in the response from the request in Step 1.
    task_id = post_response.json()['id']
    task_id_url = f"{BASE_URL}{task_id}"
    put_payload = json.dumps({
        "input_spec": {
            "style": style_id,
            "prompt": prompt,
            "target_image_weight": 0.1,
            "width": 960,
            "height": 1560
    }})
    requests.request(
        "PUT", task_id_url, headers=HEADERS, data=put_payload)

    # Step 4) Keep polling for images until the generation completes
    while True:
        response_json = requests.request(
            "GET", task_id_url, headers=HEADERS).json()

        state = response_json["state"]

        if state == "completed":
            r = requests.request(
                "GET", response_json["result"])
            print(r)
            with open("image.jpg", "wb") as image_file:
                image_file.write(r.content)
            return 'image.jpg'
            print("image saved successfully :)")
            break

        elif state =="failed":
            print("generation failed :(")
            break

        time.sleep(3)
    
    # Step 5) Enjoy your beautiful artwork :3


m_offets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]

m_numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]

class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.session = aiohttp.ClientSession()
    
    async def __get_image(self, ctx, user=None):
        messagewdwdad = await ctx.send("Working... *VROOOM*")
        await asyncio.sleep(1)
        await messagewdwdad.delete()
        if user:
            return str(user.avatar)

        await ctx.trigger_typing()

        message = ctx.message

        if len(message.attachments) > 0:
            return message.attachments[0].url

        def check(m):
            return m.channel == message.channel and m.author == message.author

        try:
            await ctx.send("Send me an image!")
            x = await self.bot.wait_for('message', check=check, timeout=15)
        except:
            return await ctx.send("Timed out...")

        if not len(x.attachments) >= 1:
            return await ctx.send("No images found.")

        return x.attachments[0].url
    def __embed_json(self, data, key="message"):
      em = discord.Embed(colour=discord.Colour.random())
      em.set_image(url=data[key])
      return em
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, msg) -> None:
        if msg.author.bot or msg.content.startswith(';'):
            return
        if ['<:5a_:1089982167288918178>',':nerd:'] in msg.content:
            await msg.reply(file=discord.File('nerd.mov'))
        
    async def __fuck_command(self, ctx, quote=None):
        await ctx.typing()
        if quote:
            await(await ctx.send("Working... *VROOOM*")).delete(delay=1)
            try:
                randmm = ["111","222","333","444","555", "666", "7", "8", "9"]
                async def niggerfuck():
                    listf = list(quote)
                    random.shuffle(listf)
                    joinf = ''.join(listf)
                    await ctx.send(f"{joinf}")

                async def kikee():
                    await ctx.send(f"{random.choice(lists.fuck)}")

                async def eifefdf():
                    nigger = random.choice(lists.prompt) + random.choice(lists.responsen)
                    print(f"{ctx.author}: {nigger}")
                    await ctx.send(f"{nigger}")

                async def speak():
                    word = "china man"
                    measure1 = time.time()
                    measure2 = time.time()
                    count = 1
                    await ctx.send(f"{ctx.author}: ")
                    while count < 2:
                        joinffed = ''.join(word)
                        await ctx.send(f"{joinffed}")
                        word = random.choice(lists.fuckcorpus)
                        if measure2 - measure1 >= 2:
                            measure1 = measure2
                            measure2 = time.time()
                            count += 1
                        else:
                            measure2 = time.time()
                async def fuckcufhf():
                    async with ctx.channel.typing():
                        try:
                            tranny = google_translator()  
                            tr1 = tranny.translate(quote, lang_tgt='en')
                            tr2 = tranny.translate(tr1, lang_src='en', lang_tgt='sp')
                            tr3 = tranny.translate(tr2, lang_src='sp', lang_tgt='sw')
                            tr4 = tranny.translate(tr3, lang_src='sw', lang_tgt='no')
                            tr5 = tranny.translate(tr4, lang_src='no', lang_tgt='de')
                            tr6 = tranny.translate(tr5, lang_src='de', lang_tgt='so')
                            tr7 = tranny.translate(tr6, lang_src='so', lang_tgt='es')
                            tr8 = tranny.translate(tr7, lang_src='es', lang_tgt='sv')
                            tr9 = tranny.translate(tr8, lang_src='sv', lang_tgt='ru')
                            tr10 = tranny.translate(tr9, lang_src='ru', lang_tgt='tr')
                            tr11 = tranny.translate(tr10, lang_src='tr', lang_tgt='th')
                            tr12 = tranny.translate(tr11, lang_src='th', lang_tgt='bg')
                            tr13 = tranny.translate(tr12, lang_src='bg', lang_tgt='fi')
                            tr14 = tranny.translate(tr13, lang_src='fi', lang_tgt='he')
                            tr15 = tranny.translate(tr14, lang_src='he', lang_tgt='hu')
                            tr16 = tranny.translate(tr15, lang_src='hu', lang_tgt='cs')
                            tr17 = tranny.translate(tr16, lang_src='cs', lang_tgt='eo')
                            tr18 = tranny.translate(tr17, lang_src='eo', lang_tgt='ka')
                            tr20 = tranny.translate(tr18, lang_src='ka', lang_tgt='en')
                            await ctx.send(f"{ctx.author}: {tr20}")
                        except Exception as e:
                            await ctx.send(f"{ctx.author}: Uh oh we got ratelimited by googleniggerniggerniggerniggerniggerniggerniggernigger((({e}")


                answer = random.choice(['1','2','3'])
                if "1" in answer:
                    await kikee()
                elif "2" in answer:
                    await eifefdf()
                else:
                    await niggerfuck()
            except:
                return

        message = ctx.message

        if len(message.attachments) > 0:
            messagewdwdad = await ctx.send("Working... *VROOOM*")
            await asyncio.sleep(1)
            await messagewdwdad.delete()
            return message.attachments[0].url

        def check(m):
            return m.channel == message.channel and m.author == message.author

        try:
            if not len(message.attachments) >= 1:
                if not quote:
                    ans = random.choice(lists.ping)
                    before = time.monotonic()
                    message = await ctx.send("Pong")
                    ping = (time.monotonic() - before) * 1000
                    await message.edit(content=f"Pinged {ans}   |   {int(ping)}ms")
        except:
            return

    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except json.JSONDecodeError:
            return await ctx.send("Couldn't find anything from the API")

        await ctx.send(r[endpoint])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def fortune(self, ctx, *, quote: commands.clean_content = None):
        """ fortune | [image] """
        async with ctx.channel.typing():
            webhooks = await ctx.channel.webhooks()
            webhook = None
      
            for hook in webhooks:
              if hook.user == self.bot.user:
                  webhook = hook
                  break
            if webhook is None: # we haven't created a webhook for this channel yet
                webhook = await ctx.channel.create_webhook(name="china man", reason="No webhook for this channel exists")
            username = ctx.message.author.display_name
            pfp = ctx.message.author.avatar.url
            file = discord.File("temp/img.jpg", filename="image.jpg")
            uri = f'whatever'
            isImage=False
            fortune = f"{random.choice(lists.fortune)}"
            if ctx.message.attachments:
                isImage=True
                image_types = ['jpg','png','jpeg', 'gif']
                for attachment in ctx.message.attachments:
                    if any(attachment.filename.lower().endswith(image) for image in image_types):
                        await attachment.save("temp/img.jpg")
                        channel = self.bot.get_channel(857815170213871618)
                        await channel.send(f'image saved')
            else:
                isImage=False
            if quote:
                await(await ctx.send("Working... *VROOOM*")).delete(delay=1)
                if isImage:
                        await webhook.send(f'{quote}\n\n{fortune}', file=file, username=str(username), avatar_url=str(pfp))
                        await ctx.message.delete()
                else:
                        await webhook.send(f'{quote}\n\n{fortune}', username=str(username), avatar_url=str(pfp))
                        await ctx.message.delete()
            else:
                if isImage:
                        await webhook.send(f'\n\n{fortune}', file=file, username=str(username), avatar_url=str(pfp))
                        await ctx.message.delete()
                else:
                        await webhook.send(f'\n\n{fortune}', username=str(username), avatar_url=str(pfp))
                        await ctx.message.delete()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def drink(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Vodka, you're feeling stronger... """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: 🥃")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks with you* 🍻")
        if user.bot:
            return await ctx.send(f"Bots are retarded, bro")

        vodka_offer = f"**{user.name}**, you got a <:rak:1069269576363282492> offer from **{ctx.author.name}**"
        vodka_offer = vodka_offer + f"\n\n**Reason:** {reason}" if reason else vodka_offer
        msg = await ctx.send(vodka_offer)

        def reaction_check(m):
            if (m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻"):
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are drinking PISS togetheR 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"Looks like **{user.name}** wants you to fuck off **{ctx.author.name}**")
        except discord.Forbidden:
            vodka_offer = f"**{user.name}**, you got a 🥃 from **{ctx.author.name}**"
            vodka_offer = vodka_offer + f"\n\n**Reason:** {reason}" if reason else vodka_offer
            await msg.edit(content=vodka_offer)
    @has_permissions(administrator=True) 
    @commands.command(pass_ctx=True)
    async def say(self, ctx,user: discord.Member, *, message):
        webhooks = await ctx.channel.webhooks()
        webhook = None
    
        for hook in webhooks:
            if hook.user == self.bot.user:
                webhook = hook
                break
        if webhook is None: # we haven't created a webhook for this channel yet
            webhook = await ctx.channel.create_webhook(name="china man", reason="No webhook for this channel exists")
        try:
            if message is None:
                return
            else:
                await ctx.message.delete()
                username = user.name
                pfp = user.avatar.url
                await webhook.send(f'{message}', username=str(username), avatar_url=str(pfp))
        except Exception as e:
            return

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def suicide(self, ctx):
        """  Just stop """
        if not isinstance(ctx.channel, discord.DMChannel):
            if ctx.author.id not in [1046850989619159171,586864381619470336]:
                embed=Embed(colour=discord.Colour.random())
                embed.description="only selected members are allowed to use this cmd"
                await ctx.send(embed=embed)
                return 
            embed=Embed(colour=discord.Colour.random())
            embed.description="can only be used in dm (only selected members are allowed to use this cmd)"
            await ctx.send(embed=embed)
            return
        async def fuckiff():
            website = "https://xbooru.com/index.php?page=post&s=random"
            soup = BeautifulSoup(urllib.request.urlopen(website))
            listLink=[]
            for link in soup.findAll('img'):
                listLink.append(link)
        
            randImageIndex = random.randint(1,(len(listLink)-1))
            imgUrl=listLink[randImageIndex]
                                    
            fuckingnf = str(imgUrl)
            clean = re.findall(r'(https?://[^\s]+)', fuckingnf)
        
            clean1 = str(clean).replace("[", "")
            clean2 = str(clean1).replace("'", "")
            clean3 = str(clean2).replace("]", "")
            clean4 = str(clean3).replace('"', "")
        
            fuckingworkaround = f"||{clean4}||"
            if "||||" in fuckingworkaround:
                await fuckiff()
            else:
                fuckme = await(await ctx.send(f"{fuckingworkaround}")).delete(delay=30)
                await self.bot.process_commands(ctx.message)
        channelid = ctx.channel.name
        await fuckiff()
        if not permissions.can_upload(ctx):
            return await ctx.send("I cannot send images here ;>;")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def poop(self, ctx):
        """  random poop image (requested by You're Poor#3096) """
        '#await fucki()'
        if not isinstance(ctx.channel, discord.DMChannel):
            if ctx.author.id not in [1046850989619159171,586864381619470336]:
                embed=Embed(colour=discord.Colour.random())
                embed.description="only selected members are allowed to use this cmd"
                await ctx.send(embed=embed)
                return 
            embed=Embed(colour=discord.Colour.random())
            embed.description="can only be used in dm (only selected members are allowed to use this cmd)"
            await ctx.send(embed=embed)
            return
        async with ctx.channel.typing():
            subreddit = await reddit.subreddit("ratemypoo")
            top = subreddit.hot()
            all_subs=[submission async for submission in top]
            random_sub = random.choice(all_subs)
            url = random_sub.url
            embed = Embed(colour=discord.Colour.random(), url=url)

            embed.set_image(url=url)
            embed.set_footer(text='Here is your poo!')
            await ctx.send(embed=embed)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command()
    async def red(self, ctx, thingy, sort):
        """  random reddit image (closed due to fuckers abusing this)"""
#        sort=sort.lower()
#        if sort not in ['new', 'hot', 'top']:
#            ctx.send('specify an actual sorting option like new, hot, or top')
#            return
#        async with ctx.channel.typing():
#            subreddit = await reddit.subreddit(thingy)
#            if sort == 'top':
#                top = subreddit.top()
#            if sort == 'hot':
#                top = subreddit.hot()
#            if sort == 'new':
#                top = subreddit.new()
#            all_subs=[i async for i in top]
#            random_sub = random.choice(all_subs)
#            name = random_sub.title
#            url = random_sub.url
#            if 'i.redd' in url:
#                embed = Embed(title=f'__{name}__', colour=discord.Colour.random(), url=url)
#
#                embed.set_image(url=url)
#                embed.set_footer(text='ffffffffffffffffffffffffffffuuuuuuuuuuckkkkkkkk')
#                await ctx.send(embed=embed)
#            else:
#                await ctx.send(url)
        await ctx.send('why not r/assbleach huh? huh? why not? why not fucking assbleach fucking liberal conservative american piece of shit fuck off')
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['f'])
    async def fuck(self, ctx, *, quote: commands.clean_content = None):
        """ you """
        async with ctx.channel.typing():
            img = await self.__fuck_command(ctx, quote)
            if not isinstance(img, str):
                return img

            async with self.session.get("https://nekobot.xyz/api/imagegen?type=magik&image=%s" % img) as r:
                res = await r.json()

            await ctx.send(embed=self.__embed_json(res))
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def speak(self, ctx, *, question: commands.clean_content):
        """ Consult chinaman """
        
        word = "china man"
        measure2 = time.time()
        measure1 = time.time()
        count = 1
        await ctx.send(f"{ctx.author}: ")
        while count < 2:
            joinffed = ''.join(word)
            await ctx.send(f"{joinffed}")
            word = random.choice(lists.fuckcorpus)
            if measure2 - measure1 >= 2:
                measure1 = measure2
                measure2 = time.time()
                count += 1
            else:
                measure2 = time.time()         
    @commands.command(aliases=['pillow'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bodypillow(self, ctx, user: discord.Member):
        """Bodypillow someone"""
        async with ctx.channel.typing():
            img = await self.__get_image(ctx, user)
            if not isinstance(img, str):
                return img
            async with self.session.get("https://nekobot.xyz/api/imagegen?type=bodypillow&url=%s" % img) as r:
                res = await r.json()

            await ctx.send(embed=self.__embed_json(res))


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ph(self, ctx, *, comment: str):
        """PronHub Comment Image"""
        async with ctx.channel.typing():
            async with self.session.get(f"https://nekobot.xyz/api/imagegen?type=phcomment"
                              f"&image={ctx.author.avatar}"
                              f"&text={comment}&username={ctx.author.name}") as r:
                res = await r.json()
            if not res["success"]:
                return await ctx.send("**Failed to successfully get image.**")
            await ctx.send(embed=self.__embed_json(res))
            
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=['google','gs'])
    async def search(self, ctx, *, search):
        """ Searches google (use ;search -image for searching image)"""
        search = search.lower()
        if ctx.author.id == 746184398852063393:
            return
        if search.startswith("-image "):
            try:
                search = search.replace("-image ", "")
                if "toddlercon" in search:
                    search = search.replace("toddlercon", "andy sixx log")
                elif "euro girl" in search or "euro woman" in search or "european girl" in search or "european woman" in search:
                    search = "slavic woman"
                elif "463015237503680522" in search:
                    #await ctx.send(f'{search}')
                    search = search.replace("463015237503680522", "anime femboy")
                elif "euro" in search:
                    search = search.replace("euro", "europe beauty")
                elif "mexico" in search:
                    search = search.replace("mexico", "venezuela")
                elif "native" in search or "native american" in search:
                    search = "native american warrior art"
                elif "america" in search:
                     if "american" in search:
                        search = search.replace("american", f"{random.choice(['fat american', 'fat black woman', 'amerimutt meme'])}")
                     else:
                         search = search.replace("america", f"{random.choice(['fat american', 'black woman', 'amerimutt', 'BLM', 'pride'])}")
                elif "kansas" in search or "okla" in search or "kan" in search:
                    search = f"{random.choice(['kansas', 'black girl'])}"
                elif "swedish girl" in search or "swedish woman" in search:
                    search = search.replace("swedish", "ukrainian")
                elif "bulgarian" in search:
                    search = search.replace("bulgarian", "bulgarian gypsy")
                elif "japanese" in search:
                    search = search.replace("japanese", f"ugly chinese")
                elif "chinese" in search:
                    search = search.replace("chinese", f"ugly chinese")
                elif "swed" in search or "swee" in search:
                    if "swedish" in search:
                        search = search.replace("swedish", "russian")
                    else:
                        search = "russian people"
                elif "stealthharder" or 'stealth' in search:
                    search = f"{random.choice(['siberian warrior art', 'nenets', 'native american warrior art', 'adolf hitler', 'genghis khan', 'viktor tsoi'])}"
                elif "bury" in search:
                    search = f"{random.choice(['chinese on horse', 'turkic', 'mongolian', 'genghis khan', 'mongolian warrior', 'blood cancer'])}"
                elif "viktor" in search:
                    if "fur" in search:
                        return await ctx.send("fuck u fuck u fuck u fuck u")
                fuckk = search.replace(" ", "_")
                website = f"https://images.search.yahoo.com/search/images?fr=yfp-t&p={str(fuckk)}"
                if "anglo" in search or "british" in search or "english" in search:
                    website = f"https://images.search.yahoo.com/search/images;_ylt=AwrExdr4Jj1ghR8AWQOJzbkF;_ylu=c2VjA3NlYXJjaARzbGsDYnV0dG9u;_ylc=X1MDOTYwNjI4NTcEX3IDMgRhY3RuA2NsawRjc3JjcHZpZAMyV2ViV2pFd0xqSXhUSWpkWC40aVJndHhNVFU0TGdBQUFBQWI0WTgzBGZyA3lmcC10BGZyMgNzYS1ncARncHJpZANjX1h6bDZmVlEwcUljUXY0ZHU3Li5BBG5fc3VnZwMxMARvcmlnaW4DaW1hZ2VzLnNlYXJjaC55YWhvby5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMEcXN0cmwDMTQEcXVlcnkDYnJpJ2lzaCUyMG1lbWUEdF9zdG1wAzE2MTQ2MjA0MTc-?p=bri%27ish+meme&fr=yfp-t&fr2=sb-top-images.search&ei=UTF-8&n=60&x=wrt"
                soup = BeautifulSoup(urllib.request.urlopen(website))
                listLink=[]
                for link in soup.findAll('img'):
                    listLink.append(link)

                randImageIndex = random.randint(1,(len(listLink)-1))
                imgUrl=listLink[randImageIndex]

                fuckingnf = str(imgUrl)
                clean = re.findall(r'(https?://[^\s]+)', fuckingnf)

                clean1 = str(clean).replace("[", "")
                clean2 = str(clean1).replace("'", "")
                clean3 = str(clean2).replace("]", "")
                clean4 = str(clean3).replace('"', "")

                embed = discord.Embed(color=0xe1a6e1)
                embed.set_image(url=f"{clean4}")
                fuckme = await ctx.send(embed=embed)

                message_list[ctx.message]=fuckme

                if not permissions.can_upload(ctx):
                    return await ctx.send("I cannot send images here ;>;")
            except Exception as e:
                await ctx.send("No results found!")
        else:
            try:
                await ctx.typing()
                search = search.replace("-image ", "")
                if "america" in search:
                    if "american" in search:
                        search = search.replace("american", f"{random.choice(['fat american', 'fat black woman', 'amerimutt meme'])}")
                    else:
                        search = search.replace("america", f"{random.choice(['fat american', 'black woman', 'amerimutt', 'BLM', 'pride'])}")
                if "us" in search:
                    if "usa" in search:
                        search = search.replace("usa", f"{random.choice(['amerimutt', 'amerifat', 'amerimutt meme'])}")
                    else:
                        search = search.replace("us", f"{random.choice(['amerimutt', 'amerifat', 'amerimutt meme'])}")
                if "united states" in search:
                    search = search.replace("united states", f"{random.choice(['amerimutt', 'amerifat', 'amerimutt meme'])}")
                    
                search = search.replace(" ", "_")
                number=0
                for j in googlee(search): 
                    number=number+1
                    if number != 5:
                        await ctx.send(f'<{j}>')
                    else:
                        break
            except Exception as e:
                await ctx.send(f"{e}No results found!")

async def setup(bot):
    await bot.add_cog(Fun_Commands(bot))