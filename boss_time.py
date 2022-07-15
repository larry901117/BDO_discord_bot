import csv
import datetime
import time

ID_CHANNEL_GUILD_BOSS_ALARM=997044853361885255
BOSS_TIME_LIST=[]
def init_boss_time():
	
	with open("boss_time_sheet.csv", newline='') as csvfile:
		# 讀取 CSV 檔案內容
		rows = csv.DictReader(csvfile)
		for row in rows:
			BOSS_TIME_LIST.append(row)
			
def week_day(datetime):
	return datetime.strftime("%w")
	
def hour(datetime):
	return datetime.strftime("%H")
	
def minute(datetime):
	return datetime.strftime("%M")
	
@client.command()
async def boss_clock():
	boss_time.init_boss_time()
	BOSS_TIME_LIST = boss_time.BOSS_TIME_LIST

	now = datetime.datetime.now()
	print(now)
	delta = datetime.timedelta(minutes=15)
	channel = client.get_channel(ID_CHANNEL_GUILD_BOSS_ALARM)
	for row in BOSS_TIME_LIST:
		if row['weekday'] == boss_time.week_day(now) and row['hour'] == boss_time.hour(now) and row['minute'] == boss_time.minute(now):
			channel.send("Boss "+row['boss'+" 已經出現"])
		if row['weekday'] == boss_time.week_day(now-delta) and row['hour'] == boss_time.hour(now-delta) and row['minute'] == boss_time.minute(now-delta):
			channel.send("Boss "+row['boss'+" 15分後出現"])
	channel.send("test")
	time.sleep(10)
	boss_clock()

