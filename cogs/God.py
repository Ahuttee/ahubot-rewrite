import discord
import random
from discord.ext import commands
import asyncio
import json
import io
import time

# Here lies commands that you can use to communicate with God, just like in TempleOS

# Dictionary for godspeak
with open("godspeak.json", 'r') as f:
    god_dictionary = json.load(f)


class God(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def godspeak(self, ctx, n: int=10):
        if n > 1000000: # An approximate number of words that should reach the 8MB filesize limit
            return await ctx.send("Max number of words reached ( 1000000 )")

        async with ctx.typing():
            words = ""
            for _ in range(n):
                words += random.choice(god_dictionary) + " "

            if len(words) > 8 * 1024 * 1024:
                await ctx.send("The text reaches the maximum filesize limit")
            elif len(words) > 2000:
                with io.StringIO(words) as f:
                    await ctx.send(file=discord.File(fp=f, filename="godspeak.txt"))
            else: await ctx.send(words)
        


    @commands.command(aliases=['godmusic'])
    async def godsong(self, ctx, n: int=1):
        if not ctx.author.voice:    return await ctx.send("Connect to a voice channel first")
        vc = await ctx.author.voice.channel.connect()
        msg = await ctx.send("Playing godsong")
        for i in range(1, n+1):
            await msg.edit(content=f"Playing godsong {i}/{n} times")
            vc.play(discord.FFmpegPCMAudio("templeos.wav"))
            while vc.is_playing():
                await asyncio.sleep(.5)
        await vc.disconnect()


def setup(client):
    client.add_cog(God(client))
