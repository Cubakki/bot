from nonebot.rule import to_me
from nonebot_adapter_gocq import Bot,Event,MessageEvent,Message
from nonebot.typing import T_State
from nonebot import on_command,on_message,on_keyword
from nonebot.permission import SUPERUSER

board_cast=on_command('--广播--',permission=SUPERUSER)
@board_cast.handle()
async def board_cast(bot : Bot,event = Event):
    boardcasting=event.get_message()
    boardcasting='---以下为广播内容---\n'+boardcasting
    groups = await bot.call_api('get_group_list',self_id=bot.self_id)
    for item in groups:
        await bot.send_msg(message_type='text',group_id=int(item['group_id']),message=boardcasting)