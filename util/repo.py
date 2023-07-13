from util import default

version = "v4.2.0"
invite = "https://discord.gg/t49uwacu"
owners = default.get("config.json").owners

def is_owner(ctx):
    return ctx.author.id in owners
