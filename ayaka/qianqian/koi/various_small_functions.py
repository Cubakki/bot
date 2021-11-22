from nonebot import on_command
from nonebot.rule import to_me
from nonebot_adapter_gocq import Event,Message,Bot,MessageEvent
import json
import re
import random as ran


jrrp1=on_command('jrrp',to_me())
jrrp2=on_command('今日人品',to_me())
@jrrp1.handle()
@jrrp2.handle()
async def jrrp(bot : Bot,event : MessageEvent):
    Sender=event.sender
    id=str(Sender.user_id)
    data_origin=open('./koi/init_data/jrrp.json','r')
    data=json.load(data_origin)
    data_origin.close()
    if Sender.sex=='female':
        sex_='姐姐'
    else:
        sex_='哥哥'

    await bot.send(message=Message(data.keys()),event=event)

    if str(id) in data.keys():
        point=data[str(id)]
    else:
        point=ran.randint(-1,100)
        data[id]=point
        data_w=json.dumps(data)
        with open('./koi/init_data/jrrp.json','w') as f:
            f.write(data_w)
            f.close()
    if 0<=point<=10:
        tail="反向幸运也是幸运..吧？明天接着努力8"
    elif point==17:
        tail="17。诶嘿嘿，17正是jk的好年纪呢"
    elif 10<point<=30:
        tail="虽然不高。还是有一点点人品的啦"
    elif 30<point<60:
        tail="再努力一点点就及格啦"
    elif 60<=point<=80:
        tail="今天的精灵格外活跃呢。是时候去捞图纸啦"
    elif 80<point<=95:
        tail="嗯。这么高的rp，今天你就是光的化身啦"
    elif 95<point<100:
        tail="！这么幸运的话，催群主女装说不定会有结果哦"
    elif point==100:
        tail="诶嘿。竟然满了诶，不如女装一下叭"
    elif point==-1:
        tail="呜诶...没想到真的有人可以是负数啊。嘛-总而言之也是一个彩蛋啦"

    await    bot.send('{}{}今天的人品值是: {} 。{}'.format(Sender.nickname,sex_,point,tail))

reset_rp=on_command('reset_rp',to_me())
@reset_rp.handle()
async def reset_rp(bot : Bot,event : Event):
    reset={}
    reset_w=json.dumps(reset)
    with open('./koi/init_data/jrrp.json', 'w') as f:
        f.write(reset_w)
        f.close()

    await bot.send(message="（强制）重置成功",event=event)

bldajian1=on_command('大建',to_me())
bldajian2=on_command('碧蓝大建',to_me())
@bldajian1.handle()
@bldajian2.handle()
async def dajian(event : Event,bot : Bot):
    jinchuan=0
    zichuan=0
    lanchuan=0
    baichuan=0
    up=0
    up_2=0
    up_c=[]
    up_2c=[]
    context='没有建造出第一艘up船'
    context2='没有建造出第二艘up船'
    for i in range(0,100):
        x=ran.randint(0,999)
        if 0<=x<=69:
            jinchuan+=1
        elif 70<=x<=189:
            zichuan+=1
        elif 190<=x<=699:
            lanchuan+=1
        elif 700<=x<=999:
            baichuan+=1

        if 0<=x<=14:
            up+=1
            up_c.append(str(i+1))

        if 15<=x<=29:
            up_2+=1
            up_2c.append(str(i+1))

        try:
            context='首次出现于第{}次建造'.format(up_c[0])
        except:
            pass

        try:
            context2='首次出现于第{}次建造'.format(up_2c[0])
        except:
            pass


    await bot.send(message=Message('{}大建了100次 \n第一艘up船{}艘,{} ; 第二艘up船{}艘，{} \n 金船{}艘，Very rare{}艘，Rare{}艘，白板{}艘'.format(session.ctx.sender['nickname'],up,context,up_2,context2,jinchuan,zichuan,lanchuan,baichuan)),event=event)
    if up == 0 and up_2 == 0:
        await bot.send(message='一艘都莫得。呵，想偷渡欧洲，真是可笑呢',event=event)

cyl1=on_command('抽炎律',to_me())
@cyl1.handle()
async def yanlv(bot: Bot,event : Event):
    judge=0
    times=0
    juesebaodi=0
    while judge==0:
        juesebaodi+=1
        if juesebaodi==10:
            x=ran.randint(0,99)
            if 0<=x<=14:
                judge=1
            juesebaodi=0
        else:
            x=ran.randint(0,999)
            if 0<=x<=14:
                judge=1
                juesebaodi=0

        times+=1
        if times==100:
            judge=1
            juesebaodi=0

    await bot.send('{}在第{}次抽到了萤火虫，花费了{}水晶'.format(event.get_user_id['nickname'],times,str(times*280)))
    if times==100:
        await bot.send(message='吃到保底了呢',event=event)

    timesss=times
    juesedabao=0
    while judge<=13:
        juesebaodi += 1
        juesedabao += 1
        if juesebaodi == 10:
            x = ran.randint(0, 99)
            if 0 <= x <= 14:
                judge+= 1
            juesebaodi = 0
            juesedabao = 0
        else:
            x = ran.randint(0, 999)
            if 0 <= x <= 14:
                judge += 1
                juesebaodi = 0
                juesedabao = 0

        timesss += 1
        if juesedabao == 100:
            judge += 1
            juesebaodi = 0;juesebaodi=0


    shangwei=0;shangwei_time=0;judge1=0
    zhongwei=0;zhongwei_time=0;judge2=0
    xiawei=0;xiawei_time=0;judge3=0
    wuqi_up=0;wuqi_time=0;judge4=0
    baodi=0;baodi_time=0
    wuqi=0
    shenghen=0
    time=0
    dabaodi=0;dabaodi_time=0

    while shangwei==0 or zhongwei==0 or xiawei==0 or wuqi==0:
        baodi+=1
        time+=1
        dabaodi+=1
        current=[shangwei,zhongwei,xiawei,wuqi_up]
        if dabaodi==50:
            dabaodi_time+=1
            baodi=0
            dabaodi=0
            index=0
            for item in current:
                control=0
                index+=1
                if item==0:
                    if control==0:
                        if index == 1:
                            shangwei += 1
                            shangwei_time = time
                            judge1 = 1
                            shenghen += 1
                        elif index == 2:
                            zhongwei += 1
                            zhongwei_time = time
                            judge2 = 1
                            shenghen += 1
                        elif index == 3:
                            xiawei += 1
                            xiawei_time = time
                            judge3 = 1
                            shenghen += 1
                        elif index == 4:
                            wuqi_up += 1
                            wuqi_time = time
                            judge4 = 1
                            wuqi += 1
                        control+=1

        elif baodi==10:
            baodi_time+=1
            x=ran.randint(0,100000)
            if 0<=x<=40000:
                wuqi+=1
            else:
                shenghen+=1
            if 0<=x<=19561:
                wuqi_up+=1
                if judge4==0:
                    dabaodi=0
                if wuqi_up==1:
                    wuqi_time=time
                    judge4=1
            if 40001<=x<=50000:
                shangwei+=1
                if judge1==1:
                    dabaodi=0
                if shangwei==1:
                    shangwei_time=time
                    judge1=1
            elif 50001<=x<=60000:
                zhongwei+=1
                if judge2==0:
                    dabaodi=0
                if zhongwei==1:
                    zhongwei_time=time
                    judge2=1
            elif 60001<=x<=70000:
                xiawei+=1
                if judge3==0:
                    dabaodi=0
                if xiawei==1:
                    xiawei_time=time
                    judge3=1
            baodi=0

        else:
            x=ran.randint(0,100000)
            if 0<=x<=9999:
                shenghen+=1
                baodi=0
            if 10000<=x<=14999:
                wuqi+=1
                baodi=0

            if 0<=x<=1239:
                shangwei += 1
                if judge1 == 1:
                    dabaodi = 0
                if shangwei == 1:
                    shangwei_time = time
                    judge1 = 1
            elif 1240<=x<=2479:
                zhongwei += 1
                if judge2 == 0:
                    dabaodi = 0
                if zhongwei == 1:
                    zhongwei_time = time
                    judge2 = 1
            elif 2480<=x<=3719:
                xiawei += 1
                if judge3 == 0:
                    dabaodi = 0
                if xiawei == 1:
                    xiawei_time = time
                    judge3 = 1
            elif 10000<=x<=12478:
                wuqi_up += 1
                if judge4 == 0:
                    dabaodi = 0
                if wuqi_up == 1:
                    wuqi_time = time
                    judge4 = 1

    context='{}共抽取了{}次扩充装备补给，吃了{}次大保底，{}次小保底。\n在第{}次抽到了「崆煌之钥」，在第{}、{}、{}次出货了姬子上中下，共花费了{}水晶，出货了{}件紫武，{}件四星圣痕'\
    .format(event.get_user_id['nickname'],time,dabaodi_time,baodi_time,wuqi_time,shangwei_time,zhongwei_time,xiawei_time,str(time*280),wuqi,shenghen)
    final='{}的炎律毕业共花费了{}水晶,需要氪金{}RMB'.format(event.get_user_id['nickname'],str(time*280+times*280),(time*28+times*28))
    await bot.send(message=context+'\n'+final,event=event)
    await bot.send(message='炎律晋级至sss级共抽取了{}次，sss毕业炎律共花费{}水晶，换算为{}RMB'.format(timesss,str(timesss*280+times*280),str(timesss*28+times*28)),event=event)

    tj = on_command('tj', to_me())
    @tj.handle()
    async def baiduyun(bot: Bot, event: Event):
        with open('./nanami/init_data/tj.json', 'r') as file:
            dic = json.load(file)
            file.close()
        name = event.get_user_id['nickname']
        print(name)
        dic['current'] = int(dic['current']) + 1
        dic['member'].append(name)
        name_list = dic['member']
        print(name_list)
        text = ''
        for m in name_list:
            text += '  ' + m
        with open('./nanami/init_data/tj.json', 'w') as file:
            writing = json.dumps(dic)
            file.write(writing)
            file.close()
        number = int(dic['current'])
        money = 180 / number
        money_f = "{:.2f}".format(money)
        await bot.send(message=' {} 已加入名单，已确认{}人，平均金额为：{}，\n目前的名单为:\n{}'.format(name, number, money_f, text),
                       event=event)


