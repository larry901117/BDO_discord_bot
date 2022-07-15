import discord
from discord.ext import commands

from core.cog_ext import cog_ext

class react(cog_ext):
	pass
def setup(bot):
	bot.add_cog(react(bot))
