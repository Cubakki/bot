from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot_adapter_gocq import Event,Message,Bot,MessageEvent,GroupMessageEvent
import json
import re
import random as ran
import shutil
import os
import ayaka.qianqian.lottery.pool_design as po
import ayaka.qianqian.koi.tools.init_data as data
import copy

def get_lotset() -> dict:
    with open('./lottery/settings.json', 'r', encoding='utf-8') as file:
        files = file.read()
    return json.loads(files)

def save_lotset(set : dict):
    with open('./lottery/settings.json', 'w', encoding='utf-8') as file:
        settings_w = json.dumps(set, ensure_ascii=False)
        file.write(settings_w)
        file.close()

lottery_settings=get_lotset()

def groupsetting_initiate(group_id):
    global lottery_settings
    lottery_settings['individual'][group_id]={"pool":"碧蓝航线","rule": {"del_N":"1","del_R":"1","mode":"1"}}
    save_lotset(lottery_settings)
    lottery_settings=get_lotset()

kachi=on_command('卡池',to_me(),permission=SUPERUSER)
@kachi.handle()
async def cardpoolset(bot:Bot,event : GroupMessageEvent):
    #natural language solution
    global lottery_settings
    raw=str(event.get_message)
    group=event.group_id
    command=re.findall('\[(\S+?)]',raw)
    if command==[]:
        command=re.findall('&#91;(\S+?)&#93;',raw)
    command=command[0]
    if str(event.user_id) not in lottery_settings["permission"]:
        await bot.send(message="您的权限不足，不能切换卡池",event=event)
        return
    try:
        tempt=lottery_settings['individual'][str(group)]
    except:
        groupsetting_initiate(group)
        await bot.send(message="检测到群设定不存在，已自动生成",event=event)
    if command in lottery_settings["all"].keys():
        lottery_settings['individual'][str(group)]["pool"]=lottery_settings["all"][command]
        value=lottery_settings["all"][command]
        if value=='碧蓝航线':
            oper=po.blhx()
            arg=str(oper.up())
        elif value=='pcr':
            oper=po.pcr()
            arg=str(oper.up())
        elif value=='smn':
            oper=po.smn()
            arg=str(oper.up())
        else:
            arg="无up"
        save_lotset(lottery_settings)
        await bot.send(message='已经切换到{}啦~\n 最后更新时间：2021.9.29 up:{}'.format(command,arg),event=event)
        lottery_settings=get_lotset()
    else:
        await bot.send(message='没有找到这个卡池哦',event=event)


chouka1=on_command('我的回合，抽卡！',to_me())
chouka2=on_command('再抽。',to_me())
chouka3=on_command('再抽！',to_me())
chouka4=on_command('抽卡',to_me())
@chouka1.handle()
@chouka2.handle()
@chouka3.handle()
@chouka4.handle()
async def wdhhck(bot:Bot,event:GroupMessageEvent):
    cache_path=data.get_cache_path();group=str(event.group_id);id=event.user_id
    global lottery_settings
    plugin_dic=copy.deepcopy(lottery_settings)
    try:
        pool=plugin_dic['individual'][group]['pool']
        del_N=plugin_dic['individual'][group]['rule']['del_N']
        del_R=plugin_dic['individual'][group]['rule']['del_R']
        mode=plugin_dic['individual'][group]['rule']['mode']
    except:
        groupsetting_initiate(group)
        pool = plugin_dic['individual'][group]
        del_N = plugin_dic['individual'][group]['rule']['del_N']
        del_R = plugin_dic['individual'][group]['rule']['del_R']
        mode = plugin_dic['individual'][group]['rule']['mode']
    path=po.assignment(pool,mode)
    command=''
    pure=[]
    try:
        for x in range(10000,10010):
            count=x-10000
            if del_N=="1":
                if 'N' in path[count]:
                    command+='已经过滤掉N卡啦\n'
                    continue
            if del_R=="1":
                if 'R' in path[count] and 'SR' not in path[count] and 'SSR' not in path[count]:
                    name=re.findall('R/(\S+?)\.',path[count])[0]
                    command+='{} get√\n'.format(name)
                    continue
            shutil.copy(path[count], cache_path+'image_up/{}.jpg'.format(x))
            pure.append(x)
            command+='[CQ:image,file=file:///'+cache_path+'image_up/{}.jpg]'.format(x)
    except:
        command=''
        pure.append('pic')
        shutil.copy(path[0],cache_path+'image_up/{}.jpg'.format('pic'))
        command+='[CQ:image,file=file:///'+cache_path+f'image_up/pic.jpg]'

    await bot.send(message=Message(f"[CQ:at,qq={id}]\n"+command),event=event)
    for x in pure:
        os.remove(cache_path+'image_up/{}.jpg'.format(x))

lotteryset=on_command('lotteryset',to_me())
@lotteryset.handle()
async def lottery_set(bot : Bot, event : GroupMessageEvent):
    global lottery_settings
    settings = copy.deepcopy(lottery_settings)
    if str(event.user_id) not in settings["permission"]:
        await bot.send(message="您的权限不足，不能切换卡池",event=event)
        return
    msg : str =event.raw_message
    group : str =str(event.group_id)
    try:
        para_list=re.findall("&#91;(\S+?):(\S+?)&#93;",msg)
    except:
        await bot.send(message='请求格式错误',event=event)
        return
    if len(para_list)==0:
        await bot.send(message='请求格式错误', event=event)
        return
    for item in para_list:
        if item[0]=="add_permission":
            if str(event.user_id) in settings["ultra_permission"]:
                settings["permission"].append(item[1])
                await bot.send(message="次级模块“lottery”中级权限已添加：{}".format(item[1]),event=event)
            else:
                await bot.send(message="您的权限不足以添加管理员",event=event)
        elif item[0]=="del_N":
            if item[1]=="1" or item[1]=="0":
                settings["individual"][group]["rule"]["del_N"]=str(item[1])
                await bot.send(message=f"设置参数已修改:\n  {group}--del_N={item[1]}", event=event)
        elif item[0]=="del_R":
            if item[1]=="1" or item[1]=="0":
                settings["individual"][group]["rule"]["del_R"] = str(item[1])
                await bot.send(message=f"设置参数已修改:\n  {group}--del_R={item[1]}", event=event)
        elif item[0]=="mode":
            if item[1]=="1" or item[1]=="0":
                settings["individual"][group]["rule"]["mode"] = str(item[1])
                await bot.send(message=f"设置参数已修改:\n  {group}--mode={item[1]}", event=event)

    save_lotset(settings)
    lottery_settings=get_lotset()

