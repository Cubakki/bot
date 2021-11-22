from nonebot_adapter_gocq import Bot,MessageEvent,Message,Event
from nonebot import on_command,on_message
import random as ran
import koi.tools.init_data as data
import koi.tools.tag_manage as tag_m
import koi.tools.pic_init as pici
import koi.tools.pixiv_api as pix
import os,re,time,socket
import urllib.request
import shutil
from nonebot.rule import to_me,keyword
import pixivpy3 as pixiv

pix_daily_ranking=on_command('今日排行')
@pix_daily_ranking.handle()
async def pix_daily_ranking(bot: Bot,event : Event):
    file_path=await pix.get_ranking_illust(bot=bot,mode='day');post='----pixiv今日排行----\n'
    if file_path[0]==True:
        for item in file_path[1]:
            post+='[CQ:image,file=file:///'+item+']'
        await bot.send(message=Message(post),event=event)
        for item in file_path[1]:
            os.remove(file_path)
    await bot.send(message='排行获取错误',event=event)
