import json

from nonebot import on_command,on_message
from nonebot.adapters import Event,Bot
from nonebot_adapter_gocq import Message
import random as ran
import koi.tools.init_data as data
import koi.tools.tag_manage as tag_m
import koi.tools.pic_init as pici
import koi.tools.pixiv_api as pix
import os,re,time,socket
import urllib.request
import shutil
from nonebot.rule import to_me,keyword

#规避检测
async def defend(bot : Bot, event : Event):
    if not bot.config.de_tuling==4:
        bot.config.de_tuling+=1
    else:
        await bot.send(message=huyanluanyu(),event= event)
        bot.config.de_tuling=0

def huyanluanyu():
    dic=json.load(data.get_resource_path()+'ecy_mad/data.json')
    dint=ran.randint(0,len(dic))
    return dic[dint]

setu=on_message(keyword('涩图','色图','setu'),priority=5)
@setu.handle()
async def picture(event : Event ,bot : Bot ):
    message=str(event.get_message());c_path=data.get_cache_path()
    uppercase = data.get_pic_count();print(message)
    if 'id' in message:
        message.replace('=','')
        try:
            index=re.findall('id(\d+)',message)[0]
            if int(index)>int(data.get_pic_count()):
                await bot.send(message="七海找不到这张图片啦",event=event)
                return None
            pici.pass_pic(int(index))
            await bot.send(message=Message('[CQ:image,file=file:///'+c_path+'image_up/%s.jpg]'%index+'数据库索引：{}/{}'.format(index, uppercase)),event=event)
            pici.pass_over(int(index))
        except:
            await bot.send(message='id读取出错啦，七海试试其它方法吧',event=event)
        finally:
            pass
    if '涩图' in message:
        try:
            message=str(re.findall('张(\S+?)涩图',message)[0])
        except:
            message=message.split('涩图')[0]
    if '色图' in message:
        try:
            message=re.findall('张(\S+?)色图',message)[0]
        except:
            message = message.split('色图')[0]

    if message!='':
        hoxina=tag_m.tag_act()
        pic_feedback=hoxina.get_tag_pic(message)
        if pic_feedback == 0:
            await bot.send(message='七海不记得有标签"{}",正在努力寻找哦'.format(message),event=event)
            respond= await pix.pix_search_from_tag(bot=bot,tag=message)
            if respond[0]==False:
                await bot.send(message='七海没有在pixiv上找到对应的图片诶，给你一张其它的吧',event=event)
                await random_pic(event,bot)
            else:
                await bot.send(message=Message('[CQ:image,file=file:///'+respond[1]+']'+f'\npixid={respond[2]}\n--来自pixiv'),event=event)
                os.remove(respond[1])
        elif pic_feedback == 1:
            await bot.send(message='没有符合全部tag的图片哦,七海会试着找一找的',event=event)
            respond = await pix.pix_search_from_tag(bot=bot, tag=message)
            if respond[0] == False:
                await bot.send(message='七海没有在pixiv上找到对应的图片诶，给你一张其它的吧',event=event)
                await random_pic(event, bot)
            else:
                await bot.send(message=Message('[CQ:image,file=file:///' + respond[1] + ']' + f'\npixid={respond[2]}\n--来自pixiv'),event=event)
                os.remove(respond[1])
        elif pic_feedback == 2:
            #没有关键词错误
            pass
        else:
            id=ran.choice(pic_feedback)
            pici.pass_pic(id)
            await bot.send(message=Message('[CQ:image,file=file:///'+c_path+'image_up/%s.jpg]'%id+'数据库索引：{}/{}'.format(id, uppercase)),event=event)
            pici.pass_over(id)
    else:
        await random_pic(event,bot)
    await defend(bot,event)


async def random_pic(event :Event,bot :Bot):
    uppercase = data.get_pic_count();c_path=data.get_cache_path()
    random = ran.randint(1, uppercase)
    pici.pass_pic(random)
    tagact = tag_m.tag_act()
    tag = tagact.get_pic_tag("id={}".format(random))
    print(event)
    await bot.send(
        message=Message('[CQ:image,file=file:///'+c_path+'image_up/{}.jpg]'.format(random) +
                        '\n数据库索引：{}/{}\n标签为：{}'.format(random, uppercase, tag)), event=event)
    pici.pass_over(random)


#@on_command("st数据库状态")
stsjk = on_command("st数据库状态", to_me())
@stsjk.handle()
async def show(bot : Bot,event : Event):
    await bot.send(message='欧尼酱。七海现在记住了{}张图片哦'.format(data.get_pic_count()),event=event)


stlr=on_command('色图录入',to_me(),aliases={'涩图录入','st录入',"setu录入","喂setu","喂涩图","图片录入"})
@stlr.handle()
async def input(bot : Bot,event : Event):
    control=data.get_switch("色图写入");c_path=data.get_cache_path();s_path=data.get_scope_path()
    if int(control)==1:
        if 'CQ:image' in str(event.get_message()):
            file_list=(re.findall('url=(\S+?)]',str(event.get_message())))

            for file in file_list:
                url=file

                if 'https' not in file:
                    await bot.send(message='url是空白哒',event=event)
                    continue

                try:
                    past_index = data.get_pic_count()
                    cur_index = data.get_pic_count() + 1
                    file_name_ini = s_path + str(cur_index) + '.jpg'
                    urllib.request.urlretrieve(url, filename=file_name_ini)
                    try:
                        open(file_name_ini)
                    except:
                        await bot.send(message="这种格式七海不认识呢w",event=event)
                        os.remove(file_name_ini)
                        return None

                    data.refresh_pic_count(cur_index)

                except :
                    await bot.send(message='啊.七海好像搞错了什么..再检查一下吧',event=event)
                else:
                    pici.pass_pic(cur_index)
                    await bot.send(message=Message("录入成功啦。\n feedback：\n 数据库序列：{}-->{}".format(past_index,
                                                                         data.get_pic_count()) +
                                           '\n[CQ:image,file=file:///'+c_path+'image_up/%s.jpg]'% cur_index \
                                       + '\n 录入id：{}'.format(data.get_pic_count())+'\n 谢谢哥哥～'),event=event)
                    pici.pass_over(cur_index)
                    pass
            pici.rename()

        else:
            await bot.send(message="这不是setu哦。这种程度七海还是分得出来的！",event=event)

    else:
        await bot.send(message="哥哥说七海不能记住色色的东西哦。~",event=event)

#@on_natural_language
#async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 tuling 命令
    #return IntentCommand(30.0, '捕获', args={'message': session.msg_text})

refresh=on_command("refresh",to_me())
@refresh.handle()
async def re_init_y(bot: Bot,event : Event):
    a=pici.rename()
    if a==1:
        await bot.send(message="索引divt刷新完成",event=event)


del1=on_command('删除',aliases={'del'},rule=to_me())
@del1.handle()
async def delet(bot: Bot,event : Event):
    if not 'id' in str(event.get_message()):
        await bot.send(message="七海听不懂这个啦。",event=event)
    else:
        main_path = data.get_scope_path()
#        send_path = 'D:\\酷Q Air\\data\\image\\'
        index=str(event.get_message()).split("=")[1]
        try:
            int(index)
        except:
            await bot.send(message="id格式错误哦w",event=event)
        else:
            try:
                hoxina=tag_m.tag_act()
                hoxina.delete_item(index)
                os.remove(main_path+index+'.jpg')
#                os.remove(send_path+index+'.jpg')
            except ValueError:
                await bot.send(message="需要移除的图片不在数据库中哦",event=event)
            else:
                await bot.send(message="移除成功啦。",event=event)
    pici.rename()



'''
防阻塞设置
async def downloadpic():
    socket.setdefaulttimeout(30)
'''

hahaha=on_command('hahaha',to_me())
hahaha.handle()
async def hahaha(bot :Bot,event: Event):
    time.sleep(5)
    await bot.send(message='nuo',event=event)