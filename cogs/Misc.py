import discord
from discord.ext import commands
from udpy import UrbanClient
import random
import os
import json

udclient = UrbanClient()

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
        
        
def setup(client):
    client.add_cog(Misc(client))