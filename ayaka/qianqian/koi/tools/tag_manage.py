import json
import re
import ayaka.qianqian.koi.tools.init_data as data

def tag_init():
    f=tag_act()
    f.match_id()


class tag_act():
    def __init__(self):
        self.scope_path=data.get_scope_path()
        t2p=open(self.scope_path+'tag_sql/tags2pic_sql.json','r')
        p2t=open(self.scope_path+'tag_sql/pic2tag_sql.json','r')
        self.t2p=json.load(t2p)
        self.p2t=json.load(p2t)

#用于判断请求的tag是否存在,返回1（存在）和0（不存在）
    def tag_judge(self,tag):
        if tag in self.t2p.keys():
            return 1
        else:
            return 0

#返回tag对应的图片id,返回的数据类型是list
    def tag_search(self,tag):
        return self.t2p[tag]

#返回图片现有的tag，输入为字符串，用正则表达式分离出图片id，格式为"id=xxx"，输出的数据类型是list
    def get_pic_tag(self,string):
        id=re.findall('id=(\d+)',string)[0]
        try:
            if not int(id[0])<=data.get_pic_count():
                return 'error1'#id不在数据库中
        except:
            return 'error2'#未读取到id或id不合法
        if len(self.p2t[id])==0:
            return "无对应标签"
        return self.p2t[id]

# 返回某几个tag下对应的所有图片id，返回的数据类型是list,输入为字符串，格式为"{tag}"使用正则表达式分离
    def get_tag_pic(self,string):
        tag=re.findall('\{(\S+?)\}',string)
        if len(tag)==0:
            try:
                tag=string.split(',')
            except:
                return 2
        output=[]
        times=0
        for item in tag:
            times+=1
            try:
                tags = self.t2p[item]
            except:
                return 0
            else:
                if times==1:
                    for thing in tags:
                        output.append(thing)
                else:
                    for past in output:
                        if not past in tags:
                            output.remove(past)

        if len(output)==0:
            return 1
        else:
            return output


#返回数据库中现有的所有tag标签,返回的数据类型是list
    def get_tag_all(self):
        tag_list=[]
        for item in self.t2p.keys():
            tag_list.append(item)
        return tag_list


#进行dic-->json操作，将字典保存至本地
    def save_t2p(self,dic):
        data=json.dumps(dic)
        with open(self.scope_path+'tag_sql/tags2pic_sql.json','w') as f:
            f.write(data)
            f.close()

    def save_p2t(self,dic):
        data=json.dumps(dic)
        with open(self.scope_path+'tag_sql/pic2tag_sql.json','w') as f:
            f.write(data)
            f.close()

#向图片添加指定tag，输入一串字符（指令内容），正则表达式判断格式为“ id=xxx”和“[tag] ”,其中[tag]可以有多个,正则表达式会识别两个输入项"id"和"tag"
    def add_tag(self,string):
        id=re.findall('id=(\d+)',string)
        tag=re.findall('\{(\S+?)\}',string)
        for ids in id:
            for tags in tag:
                if tags in self.get_tag_all():
                    if id in self.t2p[tags]:
                        return 0
                    else:
                        self.t2p[tags].append(ids)
                else:
                    self.t2p[tags] = [ids]

                self.p2t[ids].append(tags)
        self.save_p2t(self.p2t)
        self.save_t2p(self.t2p)

#对指定图片删除指定tag，输入格式同add_tag,成功则返回1，失败返回错误代码
    def delete_tag(self,string):
        id = re.findall('id=(\d+)', string)[0]
        tag = re.findall('\{(\S+?)\}', string)
        try:
            if not int(id[0])<=data.get_pic_count():
                return 'error1'#id不在数据库中
        except:
            return 'error2'#未读取到id或id不合法

        if len(tag)==0:
            return 'error4'

        for items in tag:
            if not items in self.p2t[id]:
                return 'error3'#有tag不存在于指定id下
            else:
                self.p2t[id].remove(items)
                self.t2p[items].remove(id)
            if len(self.t2p[items])==0:
                del self.t2p[items]

        self.save_t2p(self.t2p)
        self.save_p2t(self.p2t)

        return 1

#为所有现有的id创建字典元素
    def match_id(self,id=data.get_pic_count()):
        limit=int(id)
        current=[item for item in self.p2t.keys()]
        for i in range(1,limit+1):
            if str(i) in current:
                continue
            else:
                self.p2t[str(i)]=[]

        self.save_p2t(self.p2t)

#返回一个最高id为[输入值]的新p2t字典
    def create_new_p2t(self,id):
        dic={}
        for i in range(1,id+1):
            dic[str(i)]=[]

        return dic
#返回self.t2p
    def t2p_out(self):
        return self.t2p

#返回self.p2t
    def p2t_out(self):
        return self.p2t

#彻底删除某一图片id及其对应tag,传入字符串形式的id
    def delete_item(self,id):
        tag_list=self.get_pic_tag('id={}'.format(id))
        self.p2t.pop(id)
        try:
            for item in tag_list:
                self.t2p[item].remove(id)
        except:
            pass
        self.save_p2t(self.p2t)
        self.save_t2p(self.t2p)
        return None
