import discord
from discord.ext import commands
from udpy import UrbanClient
import random

udclient = UrbanClient()

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['def'])
    async def define(self, ctx, *, text):
        definitions = udclient.get_definition(text)
        if len(definitions) == 0:
            await ctx.send("I couldn't find the word")
        else:
            await ctx.send(f"**{text}**\n\n{random.choice(definitions).definition}")


def setup(client):
    client.add_cog(Misc(client))