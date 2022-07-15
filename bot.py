import discord
from discord.ext import commands
import trigger
import re
import datetime
import csv
import trigger
#import boss_time
import time
import os
import json


bot = commands.Bot(command_prefix="!")

with open('setting.json','r') as jfile:
	jdata = json.load(jfile)
	
@bot.command()
async def reload(ctx):
	for Filename in os.listdir('./cmds'):
		if Filename.endswith('.py'):
			bot.reload_extension(f'cmds.{Filename[:-3]}')

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	for row in trigger.TRIGGER_LIST:
		if  message.content ==row['key']:
			await message.channel.send(row['value'])
	if message.content.startswith("!add"):
		temp = message.content.split(" ")
		if len(temp) <3:
			await message.channel.send("指令錯誤")
		else:
			key = str(temp[1])
			value = str(temp[2])
			for i in range(3,len(temp)):
				value = value+" "+str(temp[i])
			trigger.add_trigger(key,value)
			await message.channel.send("指令已新增, "+key+", "+value)
		
	if message.content.startswith("!查詢"):
		query_key = re.sub("[ ]","%20",re.sub("(!查詢[ ]+)","",message.content))
		await message.channel.send("https://forum.gamer.com.tw/search.php?bsn=19017&q="+query_key)
	
	if message.content.startswith("!!!"):
		if message.author.id != jdata["MOD_ID"]:
			return
		await message.channel.send(message.author.id)
	await bot.process_commands(message)


@bot.event
async def on_ready():
	print("bot is online")
			
@bot.event
async def on_ready():
	print("Now I'm logging as ",bot.user)
	trigger.init_trigger()
	

for Filename in os.listdir('./cmds'):
	if Filename.endswith('.py'):
		bot.load_extension(f'cmds.{Filename[:-3]}')

if __name__ == "__main__":
	print('bot starting')
	bot.run(jdata['TOKEN'])#token

