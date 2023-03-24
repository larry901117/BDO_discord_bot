from discord.ext import commands
import discord
import trigger
import os
import json
#import keep_alive
import random

intents = discord.Intents.all()


bot = commands.Bot(command_prefix="?",intents=intents)

with open('setting.json', 'r') as jfile:
    jdata = json.load(jfile)


@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cmd.{extension}')
    await ctx.send(f'{extension} is unloaded')


@bot.command()
async def reload(ctx):
    for Filename in os.listdir('./cmds'):
        if Filename.endswith('.py'):
            await bot.reload_extension(f'cmds.{Filename[:-3]}')
            await ctx.send(f'{Filename[:-3]} is loaded')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    for row in trigger.TRIGGER_LIST:
        if message.content == row['key']:
            await message.channel.send(row['value'])
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
    if message.content.endswith("運勢"):
        ret_list = ['吉','小吉','大吉','吉娃娃的那種吉','你受到了金在熙的祝福!','凶','大凶','小凶']
        ratio_list = [30,15,5,1,1,30,5,15]
        ret = random.choices(ret_list,weights=ratio_list)
        await message.channel.send(ret[0])

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print("Now I'm logging as ", bot.user)
    trigger.init_trigger()


    for Filename in os.listdir('./cmds'):
        if Filename.endswith('.py'):
            await bot.load_extension(f'cmds.{Filename[:-3]}')

if __name__ == "__main__":
    #keep_alive.keep_alive()
    print('bot starting')
    bot.run(jdata['TOKEN'])  #token
