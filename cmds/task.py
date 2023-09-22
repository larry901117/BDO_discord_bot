import os
from discord.ext import commands
from core.cog_ext import cog_ext
import asyncio, datetime, json, csv, pytz

BOSS_TIME_LIST = []

ABS_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + os.sep
SETTING_FILE = ABS_PATH + "setting.json"

with open(SETTING_FILE, 'r') as jfile:
    SETTINGS = json.load(jfile)


def init_boss_time():
    with open('boss_time_sheet.csv', newline='', encoding='UTF-8') as csvfile:
        # 讀取 CSV 檔案內容
        rows = csv.DictReader(csvfile)
        for row in rows:
            BOSS_TIME_LIST.append(row)


def fmt_time(datetime):
    return datetime.strftime("%w %H %M")


class Task(cog_ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_boss_time()
        self.bg_task = self.bot.loop.create_task(self.interval())

    async def interval(self):
        await self.bot.wait_until_ready()
        self.channel = self.bot.get_channel(SETTINGS['ID_CHANNEL_BOSS_ALARM'])
        ##await self.channel.send("Boss 鬧鐘已開啟")
        while not self.bot.is_closed():
            tw = pytz.timezone('Asia/Taipei')
            now = datetime.datetime.now(tw)
            delta = datetime.timedelta(minutes=15)
            print("now is " + fmt_time(now) + ", after 15 min is " +
                  fmt_time(now + delta),
                  end="\r")

            for row in BOSS_TIME_LIST:
                boss_appear_time = row['weekday'] + " " + row[
                    'hour'] + " " + row['minute']
                if boss_appear_time == fmt_time(now):
                    await self.channel.send("Boss " + row['boss'] + " 已經出現")
                    print(row['boss'])
                    await asyncio.sleep(60)

                elif boss_appear_time == fmt_time(now + delta):
                    await self.channel.send("Boss " + row['boss'] + " 15分後出現")
                    print(row['boss'])
                    await asyncio.sleep(60)
            if now.strftime("%H %M") == "00 00":
                await self.channel.purge(limit=100, check=lambda m: m.author == self.bot.user)
            await asyncio.sleep(5)

    @commands.command()
    async def stop_loop(self, ctx):
        self.bg_task.cancel()
        print(asyncio.all_tasks())
        self.channel = self.bot.get_channel(SETTINGS['ID_CHANNEL_BOT_TESTER'])
        await self.channel.send("Boss 鬧鐘已關閉")

    @commands.command()
    async def start_loop(self, ctx):
        self.bg_task = self.bot.loop.create_task(self.interval())
        self.channel = self.bot.get_channel(SETTINGS['ID_CHANNEL_BOT_TESTER'])


async def setup(bot):
    # await bot.add_cog(Task(bot))
    pass