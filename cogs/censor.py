import discord,json
import re
import discord.ext.commands
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import lists, repo
import random

class Censorship(commands.Cog):
    def __init__(self, bot : discord.ext.commands.Bot):
        with open('words.json','r') as f:
          f=json.load(f)
        with open('aholes.json','r') as g:
          g=json.load(g)
        """Initializer"""
        self.bot = bot
        self.censors = f
        self.aholes=g
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_update(self, before, after):
        doom = discord.utils.get(after.roles, name="Doomed")
        nine = discord.utils.get(after.roles, name="1984")
        troll = discord.utils.get(after.roles, name="Troller")
        if (doom and troll) or (doom and nine):
          await after.remove_roles(troll)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, msg) -> None:
      avatar = msg.author.avatar
      name = msg.author.display_name
      attachments = msg.attachments
      webhooks = await msg.channel.webhooks()
      webhook = None
      
      for hook in webhooks:
              if hook.user == self.bot.user:
                  webhook = hook
                  break
      if webhook is None: # we haven't created a webhook for this channel yet
          webhook = await msg.channel.create_webhook(name="china man", reason="No webhook for this channel exists")
      content = msg.content.lower()
      if msg.author.id in self.aholes:
          content=random.choice(lists.prompt) + random.choice(lists.responsen)
          await msg.delete()
          await webhook.send(content=content, username=name, avatar_url=avatar)
          
          return
      if msg.author.bot or msg.content.startswith(';'):
          return
      if '@everyone' in msg.content or '@here' in msg.content:
          return

      
      for target, censor in self.censors.items():  
            # regex of the darkest kind
            content = re.sub(
                r'\b(' + target + r')\b|(?=(' + r'.' * len(
                    target) + target + r'))(' + target + r')|(?<=(' + target + r'))(' + target + r')', censor,
                content)
            content = re.sub(r'\b(' + target + r')s\b|(?=(' + r'.' * (
                    len(target) + 1) + target + r's))(' + target + r's)|(?<=(' + target + r's))(' + target + r's)',
                                        censor + "s", content)  

      files = [await attachment.to_file() for attachment in attachments]
      if content == msg.content.lower():
            return
          
      # something has changed in the message -> something has been censored

      
      try:
          
          await msg.delete()
      except:
          pass  # message was already deleted
          # every other exception means something more serious is wrong, let the error handler deal with it
      
      await webhook.send(content=content, username=name, avatar_url=avatar, files=files)
      
    @commands.command()
    @has_permissions(administrator=True) 
    async def add_censor(self, ctx: commands.Context, target: str.lower = None, censor:str.lower = None):
      await ctx.message.delete(delay=10)
      if target is None or censor is None:
        await (await ctx.send("Command requires both a target to censor and a result censor")).delete(delay=5)
        return
      self.censors[re.escape(target)] = censor
      await (await ctx.send (f"Added the following censor: {target}-> {censor}")).delete(delay=5)
      with open('words.json','w') as f:
        json.dump(self.censors, f)
    @commands.command ()
    @has_permissions(administrator=True) 
    async def remove_censor (self, ctx: commands.Context, target: str.lower = None):
        await ctx.message.delete(delay=10)
        if target is None:
          await (await ctx.send("Command requires a censor to remove")).delete(delay=5)
          return
        try:
          with open('words.json','r') as f:
            f=json.load(f)
          del f[re.escape(target)]
          del self.censors[re.escape(target)]
          with open('words.json','w') as w:
            json.dump(f,w)
        except:
          await (await ctx.send(f"Censor does not exist: {target}")).delete(delay=5)
          return
        await (await ctx.send(f"Removed the following censor: {target}")).delete (delay=5)
    @commands.command ()
    @has_permissions(administrator=True) 
    async def retard(self, ctx: commands.Context, target: discord.Member = None):
        """turns mentally fixed back to mentally ill"""
        await ctx.message.delete(delay=10)
        if target is None:
          await (await ctx.send("command can only turn those rehab dorks into retards.")).delete(delay=5)
          g=''.join([f'{i+1}. {v}\n' for i,v in enumerate(self.aholes)])
          await ctx.send(f"target ID's:\n{g}")
          return
        if target is not int:
          men=target.mention
          name=target.name
          target=target.id
        try:
          with open('aholes.json','r') as f:
            f=json.load(f)
          f.remove(target)
          self.aholes.remove(target)
          with open('aholes.json','w') as w:
            json.dump(f,w)
        except:
          await ctx.send(f"{name} is already retarded")
          return
        await ctx.send(f"{men} is now back to being retarded")

    
    @commands.command()
    @has_permissions(administrator=True) 
    async def therapy(self,ctx: commands.Context, target: discord.Member):
      """makes target go for therapy"""
      if target is None:
        await (await ctx.send("Command requires a retard to target")).delete(delay=5)
        return
      if target is not int:
        men=target.mention
        target=target.id
      self.aholes.append(target)
      await ctx.send (f"{men} has now gone for therapy. they are now a changed person and will speak from their heart from now on.")
      with open('aholes.json','w') as f:
        json.dump(self.aholes, f)
    @commands.command()
    @has_permissions(administrator=True) 
    async def get_censors(self, ctx: commands.Context):
      txt="```"
      for target, censor in self.censors.items():
        txt += f"\n{target}-> {censor}"
      txt += "\n```"
      await ctx.send(txt, mention_author=True)
  
      


async def setup(bot):
    await bot.add_cog(Censorship(bot))