import json
import os
import re
import sys
import random
import time
import discord
from discord.ext import commands
from core.cog_ext import cog_ext


ABS_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + os.sep
SETTING_FILE = ABS_PATH + "setting.json"



with open(SETTING_FILE, 'r') as jfile:
    SETTINGS = json.load(jfile)

def reload_setting():
    global SETTINGS
    with open(SETTING_FILE, 'r') as jfile:
        SETTINGS = json.load(jfile)

def is_mod(user_id):
    return user_id in SETTINGS['MOD_ID']


class React(cog_ext):
    @commands.command()
    async def add_trigger(self, ctx):
        sys.path.append("..")
        import trigger
        temp = ctx.message.content.split(" ")
        if len(temp) < 3:
            await ctx.channel.send("指令錯誤")
        else:
            key = str(temp[1])
            value = str(temp[2])
            for i in range(3, len(temp)):
                value = value + " " + str(temp[i])
            trigger.add_trigger(key, value)
            await ctx.channel.send("指令已新增, " + key + ", " + value)

    @commands.command()
    async def remove_trigger(self, ctx):
        sys.path.append("..")
        import trigger
        temp = ctx.message.content.split(" ")
        if len(temp) < 2:
            await ctx.channel.send("指令錯誤")
        else:
            key = str(temp[1])
            trigger.remove_trigger(key)
            await ctx.channel.send("指令已移除, " + key)

    @commands.command()
    async def advice(self, ctx):
        ctx.channel = ctx.bot.get_channel(SETTINGS["ID_CHANNEL_GUILD_ADVICE"])
        await ctx.send(re.sub(r"(\?advice\s+)", "", ctx.message.content))

    @commands.command()
    async def search(self, ctx):
        if ctx.message.content == "?search":
            await ctx.message.channel.send("Error ! 請輸入查詢內容")
        else:
            query_key = re.sub(" ", "%20", re.sub(r"(\?search\s+)", "", ctx.message.content))
            await ctx.message.channel.send("https://forum.gamer.com.tw/search.php?bsn=19017&q=" + query_key)

    @commands.command()
    async def search_player(self, ctx):
        if ctx.message.content == "?search_player":
            await ctx.message.channel.send("Error ! 請輸入查詢內容")
        else:
            query_key = re.sub(" ", "%20", re.sub(r"(\?search_player\s+)", "", ctx.message.content))
            await ctx.message.channel.send("https://www.tw.playblackdesert.com/Adventure?searchType=2&searchKeyword=" + query_key)

    @commands.command()
    async def mod(self, ctx):
        if is_mod(ctx.author.id):
            await ctx.send(ctx.message.author.id)
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")

    @commands.command()
    async def purge(self, ctx, num: int):
        if is_mod(ctx.author.id):
            await ctx.channel.purge(limit=num + 1)
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")

    @commands.command()
    async def get_user_id(self, ctx):
        if is_mod(ctx.author.id):
            keyword = re.sub(r"(\?get_user_id\s+)", "", ctx.message.content)
            if discord.utils.get(ctx.message.guild.members, name=keyword):
                member = discord.utils.get(ctx.message.guild.members, name=keyword)
                return_message = \
                    f"name:{member.name}, display name:{member.display_name}, id:{member.id}"
            elif discord.utils.get(ctx.message.guild.members, display_name=keyword):
                member = discord.utils.get(ctx.message.guild.members, display_name=keyword)
                return_message = \
                    f"name:{member.name}, display name:{member.display_name}, id:{member.id}"
            else:
                return_message = "User not found"
            await ctx.message.channel.send(return_message)
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")

    @commands.command()
    async def tag_user(self, ctx):
        keyword = re.sub(r"(\?tag_user\s+)", "", ctx.message.content)
        user = discord.utils.get(ctx.message.guild.members, name=keyword)
        embed = discord.Embed(title=":loudspeaker: 汪!汪汪!!", type="rich", color=0x8400ff,
                              description=f"歡迎<@{user.id}> 加入十九層開發建設!\n"
                                          f"請記得詳閱公會規定\n"
                                          f"如果想找攻略，這邊也有我們整理過的攻略，歡迎參考",
                              )
        embed.set_thumbnail(url="https://img.freepik.com/premium-photo/close-up-angry-chihuahua-growling-2-years-old"
                                "-front-white-wall_191971-1367.jpg?w=826")
        view = discord.ui.View()
        link_to_rule_btn = discord.ui.Button(label="公會規定",
                                             url="https://discord.com/channels/992809924230914088/996643108471193691")
        link_to_doc_btn = discord.ui.Button(label="遊戲攻略",
                                            url="https://docs.google.com/spreadsheets/d/176GT6s7ulPK3Hj18UZppDSQRD"
                                                "-KtgMOjlagjhhS8fNM/edit#gid=1195001495")
        view.add_item(link_to_rule_btn)
        view.add_item(link_to_doc_btn)
        await ctx.message.channel.send(view=view, embed=embed)
        import random
        image_list = os.listdir("images")
        image = random.choices(image_list)[0]
        await ctx.message.channel.send(file=discord.File("images"+os.sep+image))

    @commands.command()
    async def FBI(self, ctx):
        if ctx.message.author.id in SETTINGS["POLICE_IDs"]:
            if ctx.message.author.voice.channel.members:
                member_list = ctx.message.author.voice.channel.members
                lucky_one = random.choice(member_list) 
                lucky_one.voice.mute = True
                await ctx.message.channel.send(f"{lucky_one.display_name} 已經被警吉逮捕,靜音10秒")
                time.sleep(10)
                lucky_one.voice.mute = False
                await ctx.message.channel.send(f"{lucky_one.display_name} 已經假釋出獄")
            else:
                print("User has not joined a voice channel")

    @commands.command()
    async def add_police(self, ctx):
        if is_mod(ctx.author.id):
            try:
                keyword = re.sub(r"(\?add_police\s+)", "", ctx.message.content)
                user = discord.utils.get(ctx.message.guild.members, name=keyword)
                with open(SETTING_FILE, 'w') as jfile:
                    jfile["POLICE_IDs"].append(user)
            except Exception as e:
                print(str(e))
            reload_setting()
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")
            
    @commands.command()
    async def add_mod(self, ctx):
        if is_mod(ctx.author.id):
            try:
                keyword = re.sub(r"(\?add_mod\s+)", "", ctx.message.content)
                user = discord.utils.get(ctx.message.guild.members, name=keyword)
                with open(SETTING_FILE, 'w') as jfile:
                    jfile["MOD_ID"].append(user)
            except Exception as e:
                print(str(e))
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")
        reload_setting()
            

async def setup(bot):
    await bot.add_cog(React(bot))
