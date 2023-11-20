from discord.ext import commands
from core.cog_ext import cog_ext


class Main(cog_ext):
    @commands.hybrid_command(name="ping",help="查詢bot ping")
    async def ping(self, ctx):
        await ctx.send(ctx.bot.latency)


async def setup(bot):
    await bot.add_cog(Main(bot))
