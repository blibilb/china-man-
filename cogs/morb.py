import os
import io
import random
import discord
import json
import aiohttp
import re
import math

from discord.ext import commands
from discord.ext.commands import check, CheckFailure
from PIL import Image, ImageDraw, ImageOps, ImageChops, ImageFont
from util import default
from random import randrange

class Mebious_Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.session = aiohttp.ClientSession()
        self.path = "mebious"
        self.font_path = [f"{self.path}/CozetteVector.ttf", f"{self.path}/cocon.ttf", f"{self.path}/spacedock.ttf", 
        f"{self.path}/neuropol.ttf", f"{self.path}/hilogi.ttf", f"{self.path}/pixelpoiiz.ttf", f"{self.path}/loveletter.ttf",]
        
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def morb(self, ctx, *args):
        """ morb - image or text """
        async with ctx.channel.typing():
            if len(ctx.message.attachments) > 0:
                file_num = 0
                for attachment in ctx.message.attachments:
                    file_num += 1
                    file_name = f"{random.randint(1, 100000000000000000)}.png"
                    rgb = [randrange(50, 150), randrange(180, 256), randrange(50, 150)]
                    image_data = await attachment.read()
                    img = Image.open(io.BytesIO(image_data))

                    amount = random.uniform(0, 0.006)
                    width, height = img.size
                    for x in range(width):
                        for y in range(height):
                            random_value = random.random()
                            if random_value < amount:
                                random_color = random.random()
                                if random_color < 0.5:
                                    img.putpixel((x, y), 255)
                                else:
                                    img.putpixel((x, y), 0)

                    img = img.convert("L")
                    img = ImageOps.colorize(img, (0, 0, 0), (rgb))
                    img = img.convert("RGBA")
                    img.save(f"{self.path}/{file_name}")
                await ctx.reply(f"{ctx.author.mention}, saved {file_num} image(s)!")
            
            elif len(args) > 0:
                
                text = " ".join(args)
                with open(f"{self.path}/strings.json", "r") as f:
                    data = json.load(f)
                data.append(text)
                with open(f"{self.path}/strings.json", "w") as f:
                    json.dump(data, f)
                await ctx.reply(f"{ctx.author.mention}, text saved!")
                k=json.load(open('mebious/strings.json','r')) 


            else:
                image = Image.new("RGB", (2000, 1000), (0, 0, 0))
                draw = ImageDraw.Draw(image)
                file_names = os.listdir(f"{self.path}")
                file_names.remove("final_image.png")
                file_names.remove("whitenoise.png")
                png_files = [file for file in file_names if file.endswith(".png")]
                selected_files = random.sample(png_files, len(png_files))
                bg_image = Image.open(f"{self.path}/whitenoise.png")
                bg_tiles_x = int(math.ceil(2000 / bg_image.width))
                bg_tiles_y = int(math.ceil(1000 / bg_image.height))
                with open(f"{self.path}/strings.json", "r") as f:
                    data = json.load(f)
                for x in range(bg_tiles_x):
                    for y in range(bg_tiles_y):
                        image.paste(bg_image, (x*bg_image.width, y*bg_image.height))

                for file_name in selected_files:
                    img = Image.open(f"{self.path}/{file_name}").convert("RGBA")
                    aspect_ratio = img.width / img.height
                    min_size = 50
                    max_size = 500
                    width = int(random.uniform(min_size, max_size))
                    height = int(width / aspect_ratio)
                    img = img.resize((width, height), resample=Image.NEAREST)
                    x = random.randint(0, image.width - img.width)
                    y = random.randint(0, image.height - img.height)
                    img.putalpha(int(random.uniform(0.1,0.7)*255))
                    image.paste(img, (x, y), img)

                for text in data:

                    min_font_size = 20
                    max_font_size = 60
                    font_size = int(random.uniform(min_font_size, max_font_size))
                    font_path = random.choice(self.font_path)
                    font = ImageFont.truetype(font_path, font_size)

                    options = [
                        lambda x: x[::-1], # reverse the string
                        lambda x: x, # zalgo text
                        lambda x: x # leave the text as is
                    ]

                    weights = [1/3, 1/3, 1/3]

                    selected_option = random.choices(options,weights=weights)[0]
                    text = selected_option(text)

                    x = random.randint(0, 1900)
                    y = random.randint(0, 900)
                    white = random.randint(0, 255)
                    colors = [(randrange(50, 150), randrange(180, 256), randrange(50, 150)), (white, white, white)]
                    color_weights = [2, 1]
                    color = random.choices(colors, color_weights)[0]
                    transparency = random.uniform(0, 1)
                    color = color + (int(transparency * 255),)
                    draw.text((x, y), text, fill=color, font=font)
                image.save(f"{self.path}/final_image.png")
                await ctx.reply(file=discord.File(f"{self.path}/final_image.png"))

async def setup(bot):
    await bot.add_cog(Mebious_Command(bot))
