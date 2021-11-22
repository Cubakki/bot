import os
import re

#project_path--X:/xxx/xxx/bot
project_path=os.getcwd().replace('\\','/')
project_path=re.findall('(.+?bot)',project_path)[0]


def get_init_path():
    return project_path+'/ayaka/qianqian/koi/init_data/'
d_path=get_init_path()

#返回数据库中的图片数目，数据类型为integer
def get_pic_count():
    with open(d_path+'pic_count.txt','r') as file:
        cur_pic_count=int(str(file.read()))

    return cur_pic_count

def refresh_pic_count(count):
    with open(d_path+'pic_count.txt','w') as file:
        file.write(str(count))

def get_switch(key):
    with open(d_path+'switch.txt','r') as file:
        file_list=file.readlines()
        for item in file_list:
            cur_item=item.split(':')
            try:
                cur_item[0]==key
            except:
                continue
            else:
                return cur_item[1]
            finally:
                pass

        return 'unknown'

def write_switch(key,value):
    data_write=''
    with open(d_path+'switch.txt', 'r') as file:
        for line in file:
            if key in line:
                line=key+':'+str(value)
            data_write+=line

    with open(d_path+'switch.txt', 'w') as file:
        file.write(data_write)

def get_scope_path():
    return project_path+'/scope/'

def get_cache_path():
    return project_path+'/ayaka/qianqian/cache/'

def get_main_path():
    return project_path+'/ayaka/qianqian/'

def get_resource_path():
    return project_path+'/ayaka/qianqian/resource/'