import discord
from discord.ext import commands

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("I'm alive!")


def setup(bot):
    bot.add_cog(events(bot))
