from koi.tools import tag_manage,init_data,pic_init
from nonebot import on_command
from nonebot_adapter_gocq import Event,Bot,Message
from nonebot.rule import to_me
import re

#@on_command('tag索引')
sy1=on_command('获取索引',to_me())
sy2=on_command('tag索引',to_me())
sy3=on_command('索引',to_me())
@sy1.handle()
@sy2.handle()
@sy3.handle()
async def tag_all(bot: Bot , event : Event):
    hoxina=tag_manage.tag_act()
    await bot.send(message='现存的tag有:\n{}'.format(' | '.join(hoxina.get_tag_all())),event=event)

#@on_command('tag')
tag=on_command('tag',to_me())
@tag.handle()
async def tag_search(bot: Bot,event : Event):
    message = str(event.get_message())
    tag = re.findall('\{(\S+?)\}', message)
    if len(tag) == 0:
        tag = message.replace(' ','')
    for times in range(0,len(tag)):
        hoxina=tag_manage.tag_act()
        judge=hoxina.tag_judge(tag[times])
        if judge == 0:
            await bot.send(message='七海不记得有这个tag哦',event=event)
        else:
            id=hoxina.get_tag_pic(tag[times])
            if id==1:
                await bot.send(message='标签“{}”存在，不存在对应图片哦'.format(tag[times]),event=event)
            else:
                await bot.send(message='标签“{}”下的图片id为：{}'.format(tag[times],','.join(id)),event=event)

#@on_command('图片tag')
#@on_command('pictag')
tpt1=on_command('图片tag',to_me())
tpt2=on_command('pictag',to_me())
@tpt1.handle()
@tpt2.handle()
async def tag_search(bot: Bot,event : Event):
    message = str(event.get_message())
    hoxina = tag_manage.tag_act()
    tag=hoxina.get_pic_tag(message)
    if tag=='error1':
        await bot.send(message='七海没有找到这张图片哦。',event=event)
    elif tag=='error2':
        await bot.send(message='id输错了啦。',event=event)
    elif tag=='无对应标签':
        await bot.send(message='此图片没有对应标签哦', event=event)
    else:
        await bot.send(message='本图片的tag为：{}'.format(' | '.join(tag)),event=event)

#@on_command('删除tag')
#@on_command('deltag')
deltag1=on_command('删除tag',to_me())
deltag2=on_command('deltag',to_me())
@deltag1.handle()
@deltag2.handle()
async def delete_tag(bot: Bot,event : Event):
    message = str(event.get_message())
    hoxina = tag_manage.tag_act()
    feedback=hoxina.delete_tag(message)
    if feedback == 'error1':
        await bot.send(message='七海没有找到这张图片哦。',event=event)
    elif feedback == 'error2':
        await bot.send(message='id输错了啦。',event=event)
    elif feedback=='error3':
        await bot.send(message='有tag不存在于指定id下哦',event=event)
    elif feedback=='error4':
        await bot.send(message='tag名不合法哦',event=event)
    else:
        await bot.send(message='tag已经删除啦。',event=event)

#@on_command('添加tag')
#@on_command('addtag')
addtag1=on_command('添加tag',to_me())
addtag2=on_command('addtag',to_me())
@addtag1.handle()
@addtag2.handle()
async def add_tag(bot: Bot,event : Event):
    message=str(event.get_message())
    hoxina=tag_manage.tag_act()
    a=hoxina.add_tag(message)
    if a==0:
        await bot.send(message='这个tag已经存在了哦',event=event)
    else:
        await bot.send(message='tag添加成功，图片现有的tag为:{}'.format(','.join(hoxina.get_pic_tag(message))),event=event)

tag_represent=on_command('遍历标签',to_me())
@tag_represent.handle()
async def tag_represent(bot : Bot,event : Event):
    message = str(event.get_message())
    hoxina = tag_manage.tag_act()
    c_path=init_data.get_cache_path()
    pic_feedback = hoxina.get_tag_pic(message)
    for id in pic_feedback:
        pic_init.pass_pic(id)
        await bot.send(message=Message('[CQ:image,file=file:///' + c_path + 'image_up/%s.jpg]' % id),event=event)
        pic_init.pass_over(id)
