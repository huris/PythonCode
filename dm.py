#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import math
import sys
import os
import requests


class Music:
    def __init__(self):
        self.songer = ''  # 歌手名称
        self.songname = ''  # 歌曲名称
        self.albumname = ''  # 专辑名称
        self.songmid = ''  # 歌曲mid
        self.time = ''  # 歌曲时长
        self.min = 0  # 歌曲分钟
        self.sec = 0  # 歌曲秒数


headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
           }
# 创建session会话
session = requests.session()

# 保存该歌手的所有歌曲
music_list = []


# 下载歌曲
def download(songmid, name):
    filename = 'C400' + songmid
    # 获取vkey
    url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?loginUin=0&hostUin=0' \
          '&cid=205361747&uin=0&songmid=%s&filename=%s.m4a&guid=0' % (songmid, filename)
    r = session.get(url, headers=headers)
    # 获取vkey
    vkey = r.json()['data']['items'][0]['vkey']
    # 下载歌曲
    url = 'http://dl.stream.qqmusic.qq.com/%s.m4a?vkey=%s&guid=0&uin=0&fromtag=66' % (
        filename, vkey)
    r = session.get(url, headers=headers)
    f = open('/Users/huben/Desktop/music/' + name + '.mp3', 'wb')
    f.write(r.content)
    f.close()


# 获取歌手的全部歌曲
def get_singer_songs(singermid):
    # 获取歌手姓名和歌曲总数
    url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=0&hostUin=0&singermid=%s' \
          '&order=listen&begin=0&num=30&songstatus=1' % (singermid)
    r = session.get(url)
    # 获取歌手姓名
    song_singer = r.json()['data']['singer_name']
    # 获取歌曲总数
    songcount = r.json()['data']['total']
    # 根据歌曲总数计算总页数
    pagecount = math.ceil(int(songcount) / 30)
    # 循环页数，获取每一页歌曲信息
    for p in range(pagecount):
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?loginUin=0&hostUin=0&singermid=%s' \
              '&order=listen&begin=%s&num=30&songstatus=1' % (singermid, p * 30)
        r = session.get(url)
        # 得到每页的歌曲信息
        music_data = r.json()['data']['list']
        # songname-歌名，ablum-专辑，interval-时长，songmid歌曲id，用于下载音频文件
        # 将歌曲信息存放字典song_dict，用于入库
        for i in music_data:
            music = Music()
            music.songer = song_singer
            music.songname = i['musicData']['songname']  # 歌曲名称
            music.albumname = i['musicData']['albumname']  # 专辑名称
            music.songmid = i['musicData']['songmid']  # 歌曲mid
            music.min = int(i['musicData']['interval'])
            music.sec = music.min % 60
            music.min = music.min // 60
            music.time = str(music.min) + ':' + str(music.sec)  # 歌曲时长
            music_list.append(music)


def SingerDown(singername):
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=64750875469881298&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={}&g_tk=5381&jsonpCallback=MusicJsonCallback6689932776346519&loginUin=760734584&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    # s1 = input('请输入歌手名称\n')
    s1 = singername
    res = requests.get(url.format(s1), headers=headers).text
    SingerMid = re.search('"mid":"[0-9A-Za-z]*","name":"' + s1 + '",', res, re.IGNORECASE).group()[7:21]
    get_singer_songs(SingerMid)
    i = 0
    while i < len((music_list)):
        if os.name == 'posix':
            os.system('clear')  # Mac和Linux使用这个
        else:
            os.system('cls')  # windows使用这句
        for j in range(10):
            if i + j > len(music_list) - 1:
                break
            print(str(j + 1) + '.' + music_list[i + j].songname + '(' + music_list[i + j].time + ')')
        while True:
            s1 = input('输入你想下载歌曲的编号\n查看下一页直接按回车,查看上一页输入l\n按q或Q退出\n')
            if s1 == "":
                i = i + j + 1
                break
            elif s1 == "l":
                i = i - j - 1
                break
            elif s1 == 'Q' or s1 == 'q':
                exit()
            else:
                num = i + int(s1) - 1
                download(music_list[num].songmid, music_list[num].songname)


if __name__ == '__main__':

    if len(sys.argv) == 3:
        download(songmid=sys.argv[1], name=sys.argv[2])  # 根据歌曲名下载
    elif len(sys.argv) == 2:
        SingerDown(singername=sys.argv[1])
    else:
        print('输入有误请重新输入!')
