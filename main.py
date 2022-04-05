import discord
from discord.ext import commands
import json
import os


config = {}

# I also run this bot on a heroku server so
if 'HEROKU' in os.environ:
	config['token'] = os.environ['TOKEN']
	config['prefix'] = os.environ['PREFIX']
else:
	with open('config.json', 'r') as f:
		config = json.load(f)

client = commands.Bot(
		command_prefix=config['prefix'],
		allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True)
	)

@client.command()
async def reload(ctx, cog):
	if ctx.author.id == 203488399061942272:
		for filename in os.listdir("cogs"):
			if filename[:-3] == cog:
				client.reload_extension(f"cogs.{filename[:-3]}")
				return await ctx.send("Done")
		return await ctx.send("Cog not found")

@client.command()
async def load(ctx, cog):
	if ctx.author.id == 203488399061942272:
		for filename in os.listdir("cogs"):
			if filename[:-3] == cog:
				client.load_extension(f"cogs.{filename[:-3]}")
				return await ctx.send("Done")
		return await ctx.send("Cog not found")

@client.command()
async def unload(ctx, cog):
	if ctx.author.id == 203488399061942272:
		for filename in os.listdir("cogs"):
			if filename[:-3] == cog:
				client.unload_extension(f"cogs.{filename[:-3]}")
				return await ctx.send("Done")
		return await ctx.send("Cog not found")

for filename in os.listdir('cogs'):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

client.run(config["token"])


