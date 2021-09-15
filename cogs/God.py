import discord
import random
from discord.ext import commands


with open("dictonary.txt", "r") as f:
    god_dict = f.readlines()
god_dict_len = len(god_dict)

class God(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def godspeak(self, ctx, n: int):
        words = ""
        for i in range(n):
            words += god_dict[random.randint(0, god_dict_len-1)].replace('\n', ' ')

        if len(words) > 3000:   return await ctx.send("Message is too long")

        await ctx.send(words)

def setup(client):
    client.add_cog(God(client))
