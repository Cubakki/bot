from nonebot import on_command,on_message
from nonebot_adapter_gocq import Event,Bot,Message,MessageEvent
from nonebot.rule import to_me
from nonebot.typing import T_State
import re

global_set=on_command('设置',rule=to_me())
@global_set.handle()
async def glob_set1(bot : Bot,event : MessageEvent,state : T_State):
    msg=event.message
    if msg:
        state["body"]=msg

@global_set.got("body",prompt="请告诉七海全局设置指令")
async def glob_set2(bot : Bot,event : MessageEvent,state : T_State):
    body=state["body"]
    if str(event.user_id) in bot.config.superusers:
        if "yinyu" in body:
            if bot.config.yinyu==1:
                bot.config.yinyu=0
                await bot.send(message=f"布尔设置\'yinyu\'已更改,当前值为{bot.config.yinyu}",event=event)
            else:
                bot.config.yinyu = 1
                await bot.send(message=f"布尔设置\'yinyu\'已更改,当前值为{bot.config.yinyu}", event=event)
        elif "ydegree" in body:
            try:
                degree=int(re.findall("-(\d+)",body)[0])
                if 0<=degree<=100:
                    bot.config.yindegree=degree/100
                    await bot.send(message=f"yindegree参数已设置为{bot.config.yindegree}",event=event)
                else:
                    await bot.send(message="请告诉七海正确的设定值哦",event=event)
            except:
                await bot.send(message="指令不正确",event=event)
        elif "pixiv" in body:
            if bot.config.pixiv == 1:
                bot.config.pixiv = 0
                await bot.send(message=f"pixiv自动搜索已禁用", event=event)
            elif bot.config.pixiv == 0:
                bot.config.pixiv = 1
                await bot.send(message=f"pixiv自动搜索已启用", event=event)
    else:
        await bot.send(message="乃不是七海的饲主哦，不能更改全局设置",event=event)