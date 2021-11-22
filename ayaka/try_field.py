# -*- coding:utf-8 -*-
import re

text1=open('text.txt','r',encoding='utf-8').readlines()
text=''
print(text1)
for items in text1:
    items=items.replace('\n','')
    text+=items
print(text)
list=re.findall('\. (\S+?)——',text)
print(list)
text2=str(list)
text2=text2.replace('\'','\"')
print(text2)
