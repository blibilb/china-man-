

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
import openai,asyncpraw
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

from discord.ext.commands import check, CheckFailure
from discord import Webhook, utils, Embed

from PIL import Image, ImageDraw
import io
from google_trans_new import google_translator
import requests
import json
import time
# https://replicate.com/stability-ai/stable-diffusion/versions/f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1#input


BASE_URL = "https://api.luan.tools/api/tasks/"
HEADERS = {
    'Authorization': 'bearer oZFb5vfcICAbdga7mP05lg0vPogYHbGZ',
    'Content-Type': 'application/json'
}
path = None
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
class AI_Commands(commands.Cog):
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
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def ai(self, ctx, *, prompt):
        """stable diffusion (not working at the moment)"""
        async with ctx.channel.typing():
            messagewdwdad = await ctx.send("Working... *VROOOM*")
            ctx.send('wip')
            inputs = {
    # Input prompt
    'prompt': prompt,

    # Specify things to not see in the output
    # 'negative_prompt': ...,

    # Width of output image. Maximum size is 1024x768 or 768x1024 because
    # of memory limits
    'width': 768,

    # Height of output image. Maximum size is 1024x768 or 768x1024 because
    # of memory limits
    'height': 768,

    # Prompt strength when using init image. 1.0 corresponds to full
    # destruction of information in init image
    'prompt_strength': 0.8,

    # Number of images to output.
    # Range: 1 to 4
    'num_outputs': 1,

    # Number of denoising steps
    # Range: 1 to 500
    'num_inference_steps': 50,

    # Scale for classifier-free guidance
    # Range: 1 to 20
    'guidance_scale': 7.5,

    # Choose a scheduler.
    'scheduler': "DPMSolverMultistep",

    # Random seed. Leave blank to randomize the seed
    # 'seed': ...,
}

            # https://replicate.com/stability-ai/stable-diffusion/versions/f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1#output-schema
            
            #output = version.predict(**inputs)
            #await ctx.send(embed=self.__embed_json(data=output,key=0))
            await messagewdwdad.delete()
async def setup(bot):
    await bot.add_cog(AI_Commands(bot))