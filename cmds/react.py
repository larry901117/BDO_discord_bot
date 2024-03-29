import asyncio
import json
import os
import re
import sys
import random
import time
from typing import Optional
import discord
from discord.ext import commands
from core.cog_ext import cog_ext
import requests


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

    @commands.hybrid_command(name="查巴哈",help="透過巴哈姆特論壇查詢特定關鍵字",enabled=True)
    async def search(self, ctx, key_word:str):
        await ctx.message.channel.send("https://forum.gamer.com.tw/search.php?bsn=19017&q=" + key_word)

    @commands.hybrid_command(name="查詢家門名",help="透過官網查詢玩家家門",enabled=True)
    async def search_player(self, ctx, player_name:str):
        await ctx.message.channel.send("https://www.tw.playblackdesert.com/Adventure?searchType=2&searchKeyword=" + player_name)

    @commands.hybrid_command(name="查詢mod名單",description="mod專用",enabled=True)
    async def mod(self, ctx):
        if is_mod(ctx.author.id):
            mod_list = [discord.utils.get(ctx.message.guild.members, id=id).display_name for id in SETTINGS['MOD_ID']]
            await ctx.send(f"目前mod有: {mod_list}")
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")

    @commands.hybrid_command(name="大量移除訊息", help="mod專用-批量移除訊息",enabled=True)
    async def purge(self, ctx, num: int):
        if is_mod(ctx.author.id):
            await ctx.channel.purge(limit=num + 1)
            await ctx.message.channel.send(f"已移除{num}行訊息")
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

    @commands.hybrid_command(name="新增mod",hidden=True,help="mod專用",enabled=True)
    async def add_mod(self, ctx, member: discord.Member=None):
        if is_mod(ctx.author.id):
            try:
                # keyword = re.sub(r"(\?add_mod\s+)", "", ctx.message.content)
                # user = discord.utils.get(ctx.message.guild.members, name=keyword)
                SETTINGS["MOD_ID"].append(member.id)
                with open(SETTING_FILE, 'w') as file:
                    file.write(json.dumps(SETTINGS, separators=(',', ':'), indent=2))
            except Exception as e:
                print(str(e))
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")
        reload_setting()
    
    @commands.hybrid_command(name="移除mod",hidden=True,help="mod專用",enabled=True)
    async def rm_mod(self, ctx, member: discord.Member=None):
        if is_mod(ctx.author.id):
            try:
                SETTINGS["MOD_ID"].remove(member.id)
                with open(SETTING_FILE, 'w') as file:
                    file.write(json.dumps(SETTINGS, separators=(',', ':'), indent=2))
            except Exception as e:
                print(str(e))
        else:
            await ctx.message.channel.send("This function only can be used by MOD.")
        reload_setting()


    @commands.hybrid_command(name="領身分組",help="領取身分組以獲得特定通知",enabled=True)
    async def add_role(self, ctx):
        embed = discord.Embed(title="來拿身分組~~", type="rich", color=0x8400ff,
                              description=f"點下面的按鈕就可以收到特定的通知喔\n"
                                        "\n"
                                        "討海人 - 部長的不定時3+3通知\n"
                                        "廢墟飛機 - 薯片帶你去廢墟挖夢想\n"
                                        "機器人工程師 - 讓你可以控制機器龍\n",
                              )
        await ctx.send(view=button_view(),embed = embed)


async def setup(bot):
    await bot.add_cog(React(bot))

class button_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label = "討海人", style = discord.ButtonStyle.green, custom_id = "sailer_button")
    async def sailer(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name="討海人")
        await user.add_roles(role)
        await interaction.response.send_message(f"I have given you {role.mention}!", ephemeral = True)

    @discord.ui.button(label = "廢墟飛機", style = discord.ButtonStyle.gray, custom_id = "airplane_button")
    async def airplane(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name="廢墟飛機")
        await user.add_roles(role)
        await interaction.response.send_message(f"I have given you {role.mention}!", ephemeral = True)
        
    @discord.ui.button(label = "機器人工程師",  custom_id = "engineer_button")
    async def enginner(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name="機器人工程師")
        await user.add_roles(role)
        await interaction.response.send_message(f"I have given you {role.mention}!", ephemeral = True)


    # @commands.command()
    # async def FBI(self, ctx, member: discord.Member=None):
    #     if ctx.message.author.id in SETTINGS["POLICE_IDs"]:
    #         Muted = discord.utils.get(ctx.guild.roles, name="Muted")
    #         if member is None:
    #             if ctx.message.author.voice.channel is not None:
    #                 member_list = ctx.message.author.voice.channel.members
    #                 member = random.choice(member_list) 
    #             else:
    #                 print("User has not joined a voice channel")
    #         try:
    #             await member.edit(mute=True)
    #             mute_time = random.randint(1,100)
    #             await ctx.message.channel.send(f"{member.display_name} 已經被警吉逮捕,靜音{mute_time}秒")
    #             await asyncio.sleep(int(mute_time))
    #             await member.edit(mute=False)
    #             await ctx.message.channel.send(f"{member.display_name} 已經假釋出獄")
    #         except Exception:
    #             print(sys.exc_info())

    # @commands.command()
    # async def add_police(self, ctx):
    #     if is_mod(ctx.author.id):
    #         try:
    #             keyword = re.sub(r"(\?add_police\s+)", "", ctx.message.content)
    #             user = discord.utils.get(ctx.message.guild.members, name=keyword)
    #             SETTINGS["POLICE_IDs"].append(user.id)
    #             with open(SETTING_FILE, 'w') as file:
    #                 file.write(json.dumps(SETTINGS, separators=(',', ':'), indent=2))
    #         except Exception as e:
    #             print(str(e))
    #         reload_setting()
    #     else:
    #         await ctx.message.channel.send("This function only can be used by MOD.")
    
    # @commands.command()
    # @commands.cooldown(1, 600, commands.BucketType.user)
    # async def 詛咒(self,ctx,member: discord.Member=None):
    #     if ctx.message.channel.id in [SETTINGS["ID_CHANNEL_BOT_LOTTERY"],SETTINGS["ID_CHANNEL_BOT_TESTER"]]:
    #         user = ctx.message.author
    #         role = discord.utils.get(user.server.roles, name="詛咒師")
    #         await user.add_roles(role)
    #         curse_pic_dir = ABS_PATH+"curse_pic"
    #         curse_list = json.load(open(ABS_PATH+"curse.json"),"r")
    #         curse_num = random.randint(0,len(curse_list["picture"])-1)
    #         file = discord.File(curse_pic_dir + os.sep + curse_list["picture"][curse_num], filename="image.png")
    #         embed = discord.Embed(type="rich", 
    #                               title=f"{member.display_name} 已經被 {user.displayname} 詛咒了", 
    #                               description=curse_list["content"][curse_num]
    #                               )
    #         embed.set_image(url=f"attachment://{file.filename}")
    #         embed.set_author(name="十九層地獄神犬詛咒")
    #         await ctx.message.channel.send(file=file, embed=embed)
    # @commands.command()
    # async def AI(self,ctx):
    #     response = requests.post("https://api.bard.ai/v1/query", json={"question": ctx.message.content})
    #     await ctx.message.channel.send(response.json()["answer"])

    # @commands.command()
    # async def police(self, ctx):
    #     if ctx.message.author.id in SETTINGS["POLICE_IDs"]:
    #         police_list = [discord.utils.get(ctx.message.guild.members, id=id).display_name for id in SETTINGS['POLICE_IDs']]
    #         await ctx.send(f"目前警吉有: {police_list}")
    #     else:
    #         await ctx.message.channel.send("This function only can be used by MOD.")

    # @commands.command()
    # async def advice(self, ctx):
    #     ctx.channel = ctx.bot.get_channel(SETTINGS["ID_CHANNEL_GUILD_ADVICE"])
    #     await ctx.send(re.sub(r"(\?advice\s+)", "", ctx.message.content))
