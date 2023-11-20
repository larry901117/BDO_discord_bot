import datetime

from discord.ext import commands
import discord
import trigger
import os
import json
# import keep_alive
import random

INTENTS = discord.Intents.all()

BOT = commands.Bot(command_prefix="?", intents=INTENTS)

TEMP_LIST = []
FORTUNE_LIST = [
    '小吉', '吉', '大吉', '小凶', '凶', '大凶',
    '吉娃娃的那種吉', '你受到了金在熙的祝福!', "特吉列車~~bubu~~"
]
FORTUNE_RATIO_LIST = [30, 15, 4, 30, 15, 4, 1 / 3, 1 / 3, 1 / 3]

ABS_PATH = os.path.abspath(os.path.dirname(__file__)) + os.sep
SETTING_FILE = ABS_PATH + "setting.json"

with open(SETTING_FILE, 'r') as jfile:
    SETTINGS = json.load(jfile)


def is_mod(user_id):
    return user_id in SETTINGS['MOD_ID']


class ReceivedText:
    def __init__(self, author, content):
        self.timestamp = datetime.datetime.now()
        self.author = author
        self.content = content


@BOT.command()
async def unload(ctx, extension):
    if is_mod(ctx.author.id):
        await BOT.unload_extension(f'cmd.{extension}')
        await ctx.send(f'{extension} is unloaded')


@BOT.command()
async def reload(ctx):
    if is_mod(ctx.author.id):
        for Filename in os.listdir('./cmds'):
            if Filename.endswith('.py'):
                await BOT.reload_extension(f'cmds.{Filename[:-3]}')
                await ctx.send(f'{Filename[:-3]} is loaded')


@BOT.event
async def on_member_join(member):
    embed = discord.Embed(title=":loudspeaker: 汪!汪汪!!", type="rich", color=0x8400ff,
                          description=f"歡迎<@{member.id}> 加入十九層開發建設!\n"
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
    await BOT.get_channel(SETTINGS["ID_CHANNEL_BOT_WELCOME"]).send(view=view, embed=embed)


@BOT.event
async def on_member_remove(member):
    await BOT.get_channel(SETTINGS["ID_CHANNEL_BOT_WELCOME"]).send(f"{member.id} has left")


@BOT.event
async def on_message(message):
    if message.author == BOT.user:
        return
    try:
        channel_name = message.channel.name
    except AttributeError:
        channel_name = "dm"
    print(f"{message.author.display_name} in {channel_name}: {message.content}")
    for row in trigger.TRIGGER_LIST:
        if row['key'] in message.content:
            await message.reply(row['value'])
    if message.content.startswith("!add"):
        temp = message.content.split(" ")
        if len(temp) < 3:
            await message.channel.send("指令錯誤")
        else:
            key = str(temp[1])
            value = str(temp[2])
            for i in range(3, len(temp)):
                value = value + " " + str(temp[i])
            trigger.add_trigger(key, value)
            await message.channel.send("指令已新增, " + key + ", " + value)
    if message.content.endswith("運勢") and message.channel.id in [SETTINGS["ID_CHANNEL_BOT_LOTTERY"],
                                                                   SETTINGS["ID_CHANNEL_BOT_TESTER"]]:
        received_content = ReceivedText(message.author.display_name, message.content)
        is_duplicate_asking = False
        global TEMP_LIST
        for content in TEMP_LIST:
            time_delta = received_content.timestamp - content.timestamp
            if time_delta < datetime.timedelta(seconds=7200) \
                    and content.author == received_content.author and content.content == received_content.content:
                is_duplicate_asking = True
        if not is_duplicate_asking:
            ret = random.choices(FORTUNE_LIST, weights=FORTUNE_RATIO_LIST)[0]
            image_list = os.listdir("images")
            image_ret = random.choices(image_list)[0]
            print(message.author.display_name + " : " + message.content)
            print(ret + ", " + image_ret)
            file = discord.File("images" + os.sep + image_ret, filename="image.png")
            embed = discord.Embed(type="rich", title=f"{message.content}是...", description=ret
                                  )
            embed.set_thumbnail(url=f"attachment://{file.filename}")
            embed.set_author(name="十九層地獄神犬占卜")
            await message.reply(file=file, embed=embed)
            TEMP_LIST.append(received_content)
        else:
            await message.reply(r"問第二次就是大凶 No doubt, bitch")
        if len(TEMP_LIST) >= 20:
            TEMP_LIST = []

    await BOT.process_commands(message)


@BOT.event
async def on_ready():
    print("Now I'm logging as ", BOT.user)
    trigger.init_trigger()

    for Filename in os.listdir(ABS_PATH + 'cmds'):
        if Filename.endswith('.py'):
            await BOT.load_extension(f'cmds.{Filename[:-3]}')
    
    try:
        synced = await BOT.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print("An error occurred while syncing: ", e)


if __name__ == "__main__":
    # keep_alive.keep_alive()
    print('bot starting')
    import dotenv
    dotenv.load_dotenv()
    BOT.run(os.getenv('TOKEN'))  # token
