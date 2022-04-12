import discord
from discord.ext import commands
from udpy import UrbanClient
import random
import os
import json
import requests
from utils import amongus
from io import BytesIO
import cleverbotfree
import sys
import asyncio

udclient = UrbanClient()
susser = amongus.AmongUs()

# A workaround for playwright
if 'HEROKU' in os.environ:
    from subprocess import Popen, PIPE
    Popen([sys.executable, "-m", "playwright", "install"], stdin=PIPE, stdout=PIPE, stderr=PIPE)


# Load the alphabetically sorted dictionary
# This dictionary is not mine. I believe it's made by tusharlock10 
# You can check it out here
# https://github.com/tusharlock10/Dictionary
# https://www.dropbox.com/s/qjdgnf6npiqymgs/data.7z

dictionary = {}

for file in os.listdir('./dictionary'):
	with open(f'./dictionary/{file}', 'r') as f:
		dictionary[f"{file}"[1]] = json.load(f)


class Misc(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases=['urban', 'ud'])
	async def urbandictionary(self, ctx, *, text):
		definitions = udclient.get_definition(text)
		if len(definitions) == 0:
			await ctx.send("I couldn't find the word")
		else:
			await ctx.send(f"**{text}**\n\n{random.choice(definitions).definition}")


	# An actual dictionary command that is useful
	@commands.command(aliases=['definition', 'def', 'word'])
	async def define(self, ctx, word: str.upper):
		if word[0] in dictionary:
			if word in dictionary[word[0]]:
				info = dictionary[word[0]][word]
				i = 1
				message = "__**Definitions**__\n"
				for sense_num in info['MEANINGS']:
					definitions = info['MEANINGS'][sense_num]
					# Definition number along with its type (noun, verb, etc)
					message += f"{i}. ({definitions[0]})\n"
					# Definition
					message += f"{definitions[1]}\n"
					i += 1
	
				# Synonyms
				if len(info['SYNONYMS']) > 0: message += "\n__**Synonyms**__\n" + ", ".join(info['SYNONYMS']) + "\n"
				# Antonyms
				if len(info['ANTONYMS']) > 0: message += "\n__**Antonyms**__\n" + ", ".join(info['ANTONYMS'])
	
				await ctx.send(message)
			else:
				await ctx.send("I couldn't find the word")
				return
		else:
			await ctx.send("I couldn't find the word")
			return
		
		
	@commands.command()
	async def avatar(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		await ctx.send(member.avatar_url)

	@commands.command(aliases=['amogusmeter'])
	async def amogus(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author

		input_file = BytesIO(requests.get(member.avatar_url).content)
		output_file = susser.convert_image(input_file)

		await ctx.send(file=discord.File(output_file, 'amogus.gif'))

	@commands.command()
	async def ask(self, ctx, *, message):
		async with cleverbotfree.async_playwright() as pw:
			clever = await cleverbotfree.CleverbotAsync(pw)
			# The first request always returns an empty message for some reason
			await clever.single_exchange(message)

			response = await clever.single_exchange(message)
			await ctx.send(response)
		clever.close()

	@commands.command()
	async def converse(self, ctx):
		opening = await ctx.send("Trying to create a session...")
		async with cleverbotfree.async_playwright() as pw:
			clever = await cleverbotfree.CleverbotAsync(pw)
			await clever.get_form()
			await opening.delete()
			await ctx.send(f"{ctx.author.mention}\nSession created. The chat will end if theres no activity for 5 minutes, type 'exit' when you're done\nSay hi!")
			# First response is always blank for some reason
			await clever.send_input("")

			while True:
				try:
					input_msg = await ctx.bot.wait_for('message',
					check=lambda m: m.channel == ctx.channel, 
					timeout=300)
					input_msg = input_msg.content.replace("\n", " ").replace("\"", " ").replace("\\", " ") # replace weird characters
				except asyncio.TimeoutError:
                    await self.browser.close()
                    await ctx.send("Timeout reached, exiting session")
                    return
					

                if input_msg == "exit":
                    await clever.browser.close()
                    await ctx.send("Ok, exiting session")
                    return

				async with ctx.typing():
					await clever.send_input(input_msg)
					response = await clever.get_response()
					if response == "": response = "⠀"

				await ctx.send(response)

			await clever.browser.close()




			

		

		


def setup(client):
	client.add_cog(Misc(client))
