import nonebot
from nonebot import require,export
from nonebot_adapter_gocq import Bot,Event,Message
import os
from koi.tools import pixiv_api as pix

'''
@ascheduler.scheduled_job("cron", hour="18",minute="30", id="001",name='pixdaily')
async def pix_daily_ranking(bot: Bot,event : Event):
    file_path=await pix.get_ranking_illust(bot=bot,mode='day');post='----pixiv今日排行----\n'
    if file_path[0]==True:
        for item in file_path[1]:
            post+='[CQ:image,file=file:///'+item+']'
        await bot.send(message=Message(post),event=event)
        for item in file_path[1]:
            os.remove(item)
    await bot.send(message='排行获取错误',event=event)
'''