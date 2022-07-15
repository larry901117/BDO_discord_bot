import discord
from discord.ext import commands
from core.cog_ext import cog_ext
import re
import json

with open('setting.json','r') as jfile:
	jdata = json.load(jfile)

class Main(cog_ext):		
	@commands.command()
	async def ping(self,ctx):
		await ctx.send(ctx.bot.latency)

	@commands.command()
	async def 建議(self,ctx):
		ctx.channel = ctx.bot.get_channel(jdata["ID_CHANNEL_GUILD_ADVICE"])
		await ctx.send(re.sub("(!建議[ ]+)","",ctx.message.content))

	
		
def setup(bot):
	bot.add_cog(Main(bot))
