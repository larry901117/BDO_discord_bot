import discord
from discord.ext import commands
from core.cog_ext import cog_ext
import re
import json

with open('setting.json', 'r') as jfile:
    jdata = json.load(jfile)


class Main(cog_ext):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(ctx.bot.latency)


async def setup(bot):
    await bot.add_cog(Main(bot))
