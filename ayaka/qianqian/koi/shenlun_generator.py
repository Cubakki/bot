import json
import random
import re
import time
from nonebot.rule import to_me
from nonebot_adapter_gocq import Bot,Event,MessageEvent,Message
from nonebot.typing import T_State
from nonebot import on_command,on_message,on_keyword
from koi.tools.init_data import get_resource_path

random.seed(time.time())

class Slscq:
    def __init__(self, json_path):
        self.data = json.load(open(json_path, 'r', encoding='utf-8'))

    def get_random_element(self, element_type: str) -> str:
        total = len(self.data[element_type]) - 1
        return self.data[element_type][random.randint(0, total)]

    def get_title(self) -> str: return self.get_random_element('title')
    def get_noun(self) -> str: return self.get_random_element('noun')
    def get_verb(self) -> str: return self.get_random_element('verb')
    def get_adverb(self, adverb_type: int) -> str: return self.get_random_element('adverb_1' if (adverb_type == 1) else 'adverb_2')
    def get_phrase(self) -> str: return self.get_random_element('phrase')
    def get_sentence(self) -> str: return self.get_random_element('sentence')
    def get_parallel_sentence(self) -> str: return self.get_random_element('parallel_sentence')
    def get_beginning(self) -> str: return self.get_random_element('beginning')
    def get_body(self) -> str: return self.get_random_element('body')
    def get_ending(self) -> str: return self.get_random_element('ending')

    def replace_xx(self, input_str: str,them: str) -> str:
        return input_str.replace('xx', them)

    def replace_vn(self, input_str: str) -> str:
        while input_str.find('vn') != -1:
            vn = '，'.join([self.get_verb() + self.get_noun() for i in range(random.randint(1, 4))])
            input_str = input_str.replace('vn', vn,1)
        return input_str

    def replace_v(self, input_str: str) -> str:
        while input_str.find('v') != -1:
            input_str = input_str.replace('v', self.get_verb(),1)
        return input_str

    def replace_n(self, input_str: str) -> str:
        while input_str.find('n') != -1:
            input_str = input_str.replace('n', self.get_noun(),1)
        return input_str

    def replace_ss(self, input_str: str) -> str:
        while input_str.find('ss') != -1:
            input_str = input_str.replace('ss', self.get_sentence(),1)
        return input_str

    def replace_sp(self, input_str: str) -> str:
        while input_str.find('sp') != -1:
            input_str = input_str.replace('sp', self.get_parallel_sentence(),1)
        return input_str

    def replace_p(self, input_str: str) -> str:
        while input_str.find('p') != -1:
            input_str = input_str.replace('p', self.get_phrase(),1)
        return input_str

    def replace_all(self, input_str: str, them: str) -> str:
        input_str = self.replace_vn(input_str)
        input_str = self.replace_v(input_str)
        input_str = self.replace_n(input_str)
        input_str = self.replace_ss(input_str)
        input_str = self.replace_sp(input_str)
        input_str = self.replace_p(input_str)
        input_str = self.replace_xx(input_str, them)
        return input_str

    def gen(self, them: str = '年轻人买房', essay_num: int = 500) -> dict:
        end_num = begin_num = essay_num * 0.15
        body_num = essay_num * 0.7

        title = self.replace_all(self.get_title(), them)
        begin = ''
        body = ''
        end = ''

        while len(begin) < begin_num: begin += self.replace_all(self.get_beginning(), them)
        while len(body) < body_num: body += self.replace_all(self.get_body(), them)
        while len(end) < end_num: end += self.replace_all(self.get_ending(), them)

        return {'title': title,'begin': begin,'body': body,'end': end}
    
    def gen_text(self, them: str = '年轻人买房', essay_num: int = 500) -> str:
        result = self.gen(them,essay_num)
        return f"{result['title']}\n\n    {result['begin']}\n    {result['body']}\n    {result['end']}"

sl_generator=on_keyword(keywords={'生成本群','工作报告'},rule=to_me())
@sl_generator.handle()
async def shenlun_generator(bot : Bot,event : MessageEvent,state : T_State):
    msg : str =str(event.get_message())
    main=re.findall('生成本群(\S+)工作报告',msg)[0]
    resource_path=get_resource_path()+'shenlun/data.json'
    arc_gen = Slscq(resource_path)
    arc_text = arc_gen.gen_text(main,500)
    await bot.send(message=arc_text,event=event)


'''
其它的语料库：

二字名词:漏斗，中台，闭环，打法，纽带，矩阵，刺激，规模，场景，维度，格局，形态，生态，体系，认知，玩法，体感，感知，调性，心智，战役，合力，赛道，基因，模型，载体，横向，通道，补位，试点，布局，联动，价值，细分，梳理，提炼，支撑，解法，脑暴，分层，心力

二字动词:复盘，赋能，加持，沉淀，倒逼，落地，串联，协同，反哺，兼容，包装，重组，履约，响应，量化，布局，联动，细分，梳理，输出，加速，共建，支撑，融合，聚合，集成，对标，聚焦，抓手，拆解，抽象，摸索，提炼，打通，打透，吃透，迁移，分发，分装，辐射，围绕，复用，渗透，扩展，开拓，皮实，共创，共建，解耦，集成，对齐，拉齐，对焦，给到，拿到，死磕

三字名词:感知度，方法论，组合拳，引爆点，点线面，精细化，差异化，平台化，结构化，影响力，耦合性，便捷性，一致性，端到端，短平快，护城河，体验感，颗粒度

四字名词:生命周期，价值转化，强化认知，资源倾斜，完善逻辑，抽离透传，复用打法，商业模式，快速响应，定性定量，关键路径，去中心化，结果导向，垂直领域，归因分析，体验度量，信息屏障，资源整合


新水平、新境界、新举措、新发展、新突破、新成绩、新成效、新方法、新成果、新形势、新要求、新期待、新关系、新体制、新机制、新知识、新本领、新进展、新实践、新风貌、新事物、新高度;


重要性、紧迫性、自觉性、主动性、坚定性、民族性、时代性、实践性、针对性、全局性、前瞻性、战略性、积极性、创造性、长期性、复杂性、艰巨性、可讲性、鼓动性、计划性、敏锐性、有效性;


法制化、规范化、制度化、程序化、集约化、正常化、有序化、智能化、优质化、常态化、科学化、年轻化、知识化、专业化、系统性、时效性;


热心、耐心、诚心、决心、红心、真軋、公心、柔心、铁心、上心、用心、痛心、童心、好心、专心、坏心、爱心、良心、关心、核心、内心、外心、中心、忠心、衷心、甘心、攻心;


政治意识、政权意识、大局意识、忧患意识、责任意识、法律意识、廉洁意识、学习意识、上进意识、管理意识;


出发点、切入点、落脚点、着眼点、结合点、关键点、着重点、着力点、根本点、支撑点


活动力、控制力、影响力、创造力、凝聚力、战斗力;


找准出发点、把握切入点、明确落脚点、找准落脚点、抓住切入点、把握着重点、找准切入点、把握着力点、抓好落脚点





'''
