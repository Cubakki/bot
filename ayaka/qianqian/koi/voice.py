import os
import shutil
import random as ran
from nonebot import on_command,on_message
from nonebot.rule import to_me
from nonebot_adapter_gocq import Message,Event,Bot
import ayaka.qianqian.koi.tools.init_data as data

async def send_voice(voice_name,bot : Bot,event : Event):
    cache_path=data.get_cache_path();main_path=data.get_main_path()
    direct_name=voice_name.split('/')[-1]
    shutil.copy(main_path+'voice_sql/'+voice_name, cache_path+'record_up')
    file = 'file:///'+cache_path+'record_up/'+direct_name
    await bot.send(message=Message('[CQ:record,file=%s]' % file), event=event)
    os.remove(cache_path+'record_up/'+direct_name)

tvr=on_command('tvr',to_me())
@tvr.handle()
async def random_voice(bot : Bot,event : Event):
    uppercase=4315
    a=ran.randint(1,uppercase)
    print(a)
    shutil.copy('E:\布狼牙的collection\解包数据\scope\七海_init\\'+str(a)+'.mp3','D:/bot/ayaka/qianqian/cache/record_up')
    file='D:/bot/ayaka/qianqian/cache/record_up/'+str(a)+'.mp3'
    await bot.send(message=Message('[CQ:record,file=%s]'%file),event=event)
    await bot.send(message=Message('七海可能会说胡话，不要在公共场合听哦='), event=event)
    os.remove('D:/bot/ayaka/qianqian/cache/record_up/'+str(a)+'.mp3')

mor=on_command('早上好',to_me())
@mor.handle()
async def mor(bot : Bot,event : Event):
    sql_path='七海/早上好/nan205_001.ogg'
    await send_voice(sql_path,bot=bot,event=event)

nig=on_command('晚安',to_me())
@nig.handle()
async def nig(bot : Bot,event : Event):
    sql_path = '七海/一起睡/nan203_140.ogg'
    await send_voice(sql_path, bot=bot, event=event)


qua=on_command('qua',to_me())
qua_button=on_command('qua_button',to_me())
@qua.handle()
@qua_button.handle()
async def qua(bot : Bot,event : Event):
    list=os.listdir('.\\voice_sql\\meamea')
    uppercase=len(list)
    a=ran.randint(1,uppercase)
    sql_path = 'meamea/'+str(list[a])

yiqishui=on_command('一起睡',to_me())
@yiqishui.handle()
async def yiqishui(bot : Bot,event : Event):
    sql_path = '七海/一起睡/nan203_140.ogg'
    await send_voice(sql_path, bot=bot, event=event)