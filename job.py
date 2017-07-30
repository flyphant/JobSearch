#!/usr/bin/env python
#coding=utf-8 
'''
Created on 2017年7月29日

@author: jaysonding
'''

import urllib2
from bs4 import BeautifulSoup

#抓取所需内容
url='http://szeb.sz.gov.cn/xxgk/flzy/rsxx2/ryzp/index.htm'

#随机从user_agent列表中抽取一个元素
request=urllib2.urlopen(url)
#print request

soup=BeautifulSoup(request,'html.parser')
ryzp=soup.find_all("div", class_="news_list")[0].ul
#print str(ryzp.find_all('a')).decode('unicode_escape')

for zp in ryzp.find_all('a'):
    print zp.previous_element,':',zp['title'],':',zp['href']
writer=open('d:\\job.html','w')
writer.write(str(soup.body))



