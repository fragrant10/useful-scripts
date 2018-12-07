# Copyright (c) 2018 fragrant
#
# -*- coding:utf-8 -*-
# @Script: fofaUrls.py
# @Author: fragrant
# @github: https://github.com/fragrant10
# @Create At: 2018-12-06 14:53:38
# @Last Modified By: fragrant
# @Last Modified At: 2018-12-07 17:00:47
# @Description: url Collection of query_url ! Have Fun!

import requests,sys,base64,re
from bs4 import BeautifulSoup

# 函数登录fofa
def login_fofa(url, username, password):
    # 第一个请求用于获得post需要的参数utf8 authenticity_token lt Cookie 
    req = s.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    utf8 = soup.find_all('input')[0]['value']
    authenticity_token = soup.find_all('input')[1]['value']
    lt = soup.find_all('input')[2]['value']
    Cookie = req.headers['Set-Cookie']
    # print(utf8,authenticity_token,lt, Cookie)
    headers = {
        'Host': 'i.nosec.org',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://i.nosec.org/login',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '255',
        'Connection': 'close',
        'Cookie': Cookie,
        'Upgrade-Insecure-Requests': '1'
    }

    post_data = {
        'utf8' : utf8,
        'authenticity_token' : authenticity_token,
        'lt' : lt,
        'service' : 'http://fofa.so/users/service',
        'username' : username,
        'password' : password,
        'button' : ''
    }

    # login i.nosec.org
    reqLogin = s.post(url, data=post_data, headers = headers, allow_redirects=False)
    # login fofa
    url2 = reqLogin.headers['Location']
    reqLogin_2 = s.get(url2)
    return reqLogin_2

# 查询 并保存结果
def query_search(query, Cookie, filename, page = '1'):
    # print(query)
    headers = {
        'Host': 'fofa.so',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Cookie': Cookie,
        'Upgrade-Insecure-Requests': '1'
    }

    if int(page) > 1:
        query = query + '&page=' + page
    reqQuery = s.get(query, headers = headers, allow_redirects=False)
    soup = BeautifulSoup(reqQuery.content, 'html.parser')
    searchResult = soup.find_all(href=re.compile("^http"))
    # print(searchResult)
    # 每次查询只有有len(searchResult)-4个结果 遍历写入filename文件里面
    for i in range(len(searchResult)-4):
        try:
            link = searchResult[i].get('href') + '\n'
            result_savetofile(filename,link)
        except Exception as erro:
            print('----END---')
            result_savetofile(filename,'----END---')
    print('Complete Page : ' + page)

# 保存文件
def result_savetofile(filename,content):
    file = open(filename, 'a+')
    file.write(content)
    file.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 fofaUrls.py 'what you want to search'")
    else:
        query = sys.argv[1]
        # query = 'app="DedeCMS" && country=CN && os=windows'
        # print(query)
        page = '5'
        filename = 'fofa_result.txt'
        username = 'email'
        password = 'passwd'
        s = requests.Session()
        login_url = 'https://i.nosec.org/login?service=http://fofa.so/users/service'
        query_base64 = str(base64.b64encode(query.encode('utf-8')),'utf-8')
        # print(query_base64)
        query_url = 'https://fofa.so/result?qbase64=' + query_base64 + '&full=true'
        # 登录并获得登陆后fofa的cookie
        loginedFofa = login_fofa(login_url, username, password)
        loginedFofaCookies = loginedFofa.headers['Set-Cookie']
        for i in range(int(page)):
            i = i+1
            query_search(query_url,loginedFofaCookies, filename, str(i))
        print('all urls asved in ' + filename)
