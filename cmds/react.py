import discord
from discord.ext import commands

from core.cog_ext import cog_ext

class react(cog_ext):
	pass
async def setup(bot):
	await bot.add_cog(react(bot))
