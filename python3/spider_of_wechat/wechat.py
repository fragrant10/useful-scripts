#!/usr/bin python
#encoding: utf-8
from wechatsogou import *
from bs4 import BeautifulSoup
import re,os,requests

wechats = WechatSogouAPI()
#获得特定公众号信息
#contents_01 = wechats.get_gzh_info('大学生信息安全题库')

#搜索公众号
#contents_10 = wechats.search_gzh('大学生信息安全题库')

#搜索微信文章
##contents_1 = wechats.search_article('大学生信息安全题库')
contents_2 = wechats.search_article('每日一测试---安全运维')
contents_3 = wechats.search_article('每日一测试---渗透测试')
contents_4 = wechats.search_article('ccsec02')
contents_5 = wechats.search_article('一道讨论题')
contents_6 = wechats.search_article('大学生信息安全题库')
contents_7 = []
for i in range(12):
    i +=1
    i = str(i)
    search_title = '2017-11-' + i + '一道讨论题'
    contents_7 += wechats.search_article(search_title)
contents_all =  contents_2 + contents_3 + contents_4 + contents_5 + contents_6 + contents_7

img_link = ['']

for i in contents_all:
##    print(i[1]['article']['title'], i[1]['article']['url'])
    if re.search('【答', i['article']['title'],re.S):
        title_na = i['article']['title']
        url = i['article']['url']
        respon = requests.get(url)
##      获得页面
        soup = BeautifulSoup(respon.text, "lxml")
        time_line = soup.find(id="post-date")
        time_ = time_line.contents
        filename = time_[0] + '/' + title_na + '.html'
##      获得图片
        img_all = soup.find_all('img')
        
##        print(img_link)
        if os.path.exists(time_[0]) == False:
            print('OK-----' + filename)
            os.mkdir(time_[0]) 
            file_ = open(filename, 'w')
            file_.write(respon.text)
            file_.close()
            tt = 0
            for link in img_all:
                tt += 1
                if tt > 10:
                    break
                if link.get('data-src') == None:
                    continue
                else:
                    img_url = link.get('data-src')
                    respon_1 = requests.get(img_url)
                    if respon_1.status_code == 200:
                        file_ = open(time_[0] + '/' + str(tt) + '123.png', 'wb')
                        file_.write(respon_1.content)
                        file_.close()
            
