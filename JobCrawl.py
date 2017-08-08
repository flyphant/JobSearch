#!/usr/bin/env python
#coding=utf-8 
'''
 * 
 * 爬取深圳市教师招聘信息
 * @version 2.7.12
 * @date 2017年8月4日
 * @author Jaysonding
 *
'''

import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin

#爬取网站,返回BeautifulSoup
def beautifulSoupUrl(url):
    
    #伪装浏览器头
    headers =  {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    request = urllib2.Request(url=url,headers=headers)  
    
    try:
        response=urllib2.urlopen(request)
        return BeautifulSoup(response,'html.parser')
    except urllib2.HTTPError as e:
        print "爬取网站",url,"异常",e
    

def crawlSzsjyj():
    '''
        Returns:bs4.element.ResultSet 返回带招聘链接的url列表
    '''
    
    #抓取所需内容
    url='http://szeb.sz.gov.cn/xxgk/flzy/rsxx2/ryzp/index.htm'
    soup=beautifulSoupUrl(url)
    ryzpTag=soup.find_all("div", class_="news_list")[0].ul
    ryzpResultSet=ryzpTag.find_all('a')
    return ryzpResultSet

def crawlPage(url):
    '''
        Args: url每一页的链接地址
                                         比如  http://szeb.sz.gov.cn/xxgk/flzy/rsxx2/ryzp/201707/t20170713_7855306.htm
        Returns: 解析一条招聘信息    
                               爬取该条链接里的符合条件的附件信息
    '''
    print "爬取页面",url
    
    try:
        hrefList=beautifulSoupUrl(url).findAll('a')
        
        for href in hrefList:
        
            #帅选出包含href的链接
            if href.has_attr('href'):
                try:
                    attLink=href['href']
                    if attLink[-4:]=='docx' or attLink[-4:]=='xlsx' or attLink[-3:]=='xls' or attLink[-3:]=='doc':
                        text=href.get_text().encode('utf-8')
                        #print 'text:',type(text),text             
                        if '成绩' not in text and '招聘' in text:
                            print 'href key:',urljoin(url,href['href'])
                            print 'text value:',text
                            #downloadFile(urljoin(zpurl,href['href']), href.get_text())
                        else:
                            #print '==不包含:',href.get_text()
                            #print '==不包含text:',type(text),text   
                            pass
                        
                except Exception as e:
                    print '解析url内容错误',url,e,href
    except Exception as e:
        print '解析url a链接失败:',url

def downloadFile(url,fileName):
    data=urllib2.urlopen(url).read()
    with open('./file/'+fileName,'wb') as code:
        code.write(data)

#解析深圳市教育局招聘信息里的每一条链接
def crawlAttachment(attachment,zpurl):
    pass
        
def analysis():
    i=0
    for zp in crawlSzsjyj():
        print "当前解析链接:",zp
        create_date=zp.previous_element #招聘发布时间 
        current_base_url='http://szeb.sz.gov.cn/xxgk/flzy/rsxx2/ryzp/' #网站当前路径
        
        url1=zp['href']
        zpurl=urljoin(current_base_url, url1)
        crawlPage(zpurl)
                
        i=i+1
        print "==============执行了",i,"次",zp,type(zp)
        
        #if(i==10):
            #break
        
    #writer=open('d:\\job.html','w')
    #writer.write(str(crawlSzsjyj().body))

if __name__ == '__main__':
    analysis()



