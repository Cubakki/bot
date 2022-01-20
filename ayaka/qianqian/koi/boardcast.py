from nonebot.rule import to_me
from nonebot_adapter_gocq import Bot,Event,MessageEvent,Message
from nonebot.typing import T_State
from nonebot import on_command,on_message,on_keyword
from nonebot.permission import SUPERUSER

#向列表中所有群发送广播，格式为 "--广播-- xxxxxxxxxx"
board_cast=on_command('--广播--',permission=SUPERUSER)
@board_cast.handle()
async def board_cast(bot : Bot,event : Event):
    boardcasting=event.get_message()
    boardcasting='---以下为广播内容---\n'+boardcasting
    groups = await bot.call_api('get_group_list',self_id=bot.self_id)
    for item in groups:
        await bot.send_msg(message_type='text',group_id=int(item['group_id']),message=boardcasting)

#向指定群发送消息，格式为  "--指向消息-- target=xxxxxxxx<分割线>xxxxxxxxxxx",分割线前为群号信息，分割线后为消息内容
specific_messeage=on_command('--指向消息--',permission=SUPERUSER)
@specific_messeage.handle()
async def specific_message(bot : Bot,event : Event):
    row=str(event.get_message())
    specific_part,message_part=row.split("<分割线>")[0],row.split("<分割线>")[1]
    target=specific_part.split("=")[1]
    await bot.send_msg(message_type='text',group_id=int(target),message=message_part)