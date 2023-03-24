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
		await ctx.send(re.sub("(?建議[ ]+)","",ctx.message.content))
	@commands.command()
	async def 查詢(self,ctx):
		if ctx.message.content == "?查詢":
			await ctx.message.channel.send("Error ! 請輸入查詢內容")
		else:
			query_key = re.sub("[ ]","%20",re.sub("([?]查詢[ ]+)","",ctx.message.content))
			await ctx.message.channel.send("https://forum.gamer.com.tw/search.php?bsn=19017&q="+query_key)

	@commands.command()
	async def mod(self,ctx):
		if ctx.author.id != jdata["MOD_ID"]:
			return
		await ctx.send(ctx.message.author.id)
	
	@commands.command()
	async def purge(self,ctx,num:int):
		await ctx.channel.purge(limit = num+1)
		
async def setup(bot):
	await bot.add_cog(Main(bot))
