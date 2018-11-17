#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 这是一个爬虫包图网视频的程序



import re
import math
import time
import urllib
import sys
import os
import requests
import random




def get_headers():
    '''
    随机获取一个headers
    '''
    user_agents =  ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent':random.choice(user_agents)}
    return headers

if __name__ == '__main__':
    op=[
         'https://ibaotu.com/sucai/953924.html',
         'https://ibaotu.com/sucai/568438.html',
         'https://ibaotu.com/sucai/137033.html',
         'https://ibaotu.com/sucai/474217.html',
         'https://ibaotu.com/sucai/292766.html',
         'https://ibaotu.com/sucai/315840.html',
         'https://ibaotu.com/sucai/134265.html',
         'https://ibaotu.com/sucai/210620.html',
         'https://ibaotu.com/sucai/619527.html',
         'https://ibaotu.com/sucai/338873.html'
       ]
    headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
           }

    for url in op:
        session = requests.session()
        header = get_headers()
        res = requests.get(url, headers=header).text
        name = re.search('<title>.*</title>', res).group()[7:-16]
        down = 'http:' + re.search('src="//.*.mp4', res).group()[5:]
        time.sleep(random.randint(0, 5))  # 暂停0~3秒的整数秒，时间区间：[0,3]
        r = session.get(down, headers=header)
        f = open('/Users/huben/Desktop/video/' + name + '.mp4', 'wb')
        f.write(r.content)
        f.close()