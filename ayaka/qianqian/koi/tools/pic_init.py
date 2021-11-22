import os,sys
import shutil
import ayaka.qianqian.koi.tools.init_data as data
import ayaka.qianqian.koi.tools.tag_manage as tag_m
from nonebot import on_command
from nonebot.adapters import Event,Message,Bot
import copy
from nonebot.rule import to_me


def rename():
    filepath = data.get_scope_path()  # 文件夹路径
    init_data_path=data.get_init_path()

    if not os.path.exists(filepath):
        print("目录不存在!!")
        sys.exit(1)

    filenames = os.listdir(filepath)
    for item in filenames:
        if not '.' in item:
            filenames.remove(item)

    default=1
    number=0
    number_sort=0
    for item in filenames:
        name=os.path.splitext(item)[0]
        try:
            int(name)
        except:
            number+=1
        else:
            number+=1
            number_sort+=1
            pass

    print("文件数目为%i" % number)

    if default==1:
        hoxina=tag_m.tag_act()
        p2t=hoxina.p2t_out()
        p2t_new=hoxina.create_new_p2t(number)
        count=0
        undefined=[]
        undefined_af=[]
        defined=[]
        p2t_fuben=copy.deepcopy(p2t)

        for thing in filenames:
            before=os.path.splitext(thing)[0] #前缀
            before_af=os.path.splitext(thing)[1] #后缀
            try:
                defined.append(int(before))
            except:
                undefined.append(before)
                undefined_af.append(before_af)

        defined.sort()

        for things in defined:
            count+=1
            name_=things

            os.rename(filepath+'{}.jpg'.format(things),filepath+'{}.jpg'.format(count))
            try:
                p2t_new[str(count)]=p2t_fuben[str(name_)]
                tags = hoxina.get_pic_tag('id={}'.format(name_))
            except:
                p2t_new[str(count)]=[]
                tags=[]

            if tags=='无对应标签':
                tags=[]

            stri=''
            for tag in tags:
                stri+='{%s}'%tag
            if stri=='':
                continue
            else:
                hoxina.delete_tag('id={},'.format(name_)+','+stri)
                hoxina.add_tag('id={}'.format(count)+','+stri)

        for undefine in range(0,len(undefined)):
            os.rename(filepath+'{}{}'.format(undefined[undefine],undefined_af[undefine]), filepath+'{}.jpg'.format(number_sort + 1))
            print(filepath+'{}'.format(undefined[undefine]) + "已更名为" + filepath+'{}.jpg'.format(number_sort + 1))
            number_sort += 1

        with open(init_data_path+'pic_count.txt', 'w') as file:
            context = str(number)
            file.write(context)
        hoxina.save_p2t(p2t_new)
        return 1



#此函数将创造一个从数据库到发送域的图片镜像
def pass_pic(id):
    shutil.copy(data.get_scope_path()+'{}.jpg'.format(id),data.get_cache_path()+'image_up/{}.jpg'.format(id))

#本函数将删除发射域中的镜像
def pass_over(id):
    os.remove(data.get_cache_path()+'image_up/{}.jpg'.format(id))


#由于数据结构变化，本函数已禁用
'''

@on_command("数据库重载")
async def reload(session:CommandSession):
    main_path = "D:\\scope\\"
    send_path = 'D:\\酷Q Air\\data\\image\\'
    file_names_main = os.listdir('D:\\scope')
    file_names_send= os.listdir('D:\\酷Q Air\\data\\image')
    for name in file_names_send:
        os.remove(send_path+name)

    for names in file_names_main:
        if '.' not in names:
            continue
        shutil.copy(main_path+names,'D:\\酷Q Air\\data\\image')

    await session.send('数据库重载成功')

'''