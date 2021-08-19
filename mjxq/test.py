#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/19 14:51
@Author   : colinxu
@File     : test.py
@Desc     : 
"""
import requests
import json

requests.packages.urllib3.disable_warnings()

# GET https://kjxq.api.wlnps.com/filter/allNames HTTP/1.1
# X-Client-Version: 1.3.2
# X-Client-Time: 1629355712100
# X-Device-Flag: 7dcca9b1-dc07-4bde-aebf-caa462ffbb93
# X-Client-Model: HUAWEIVOG-AL10
# X-API-Version: 1
# X-Client-App-Id: com.mjxq.app
# X-Client-Type: APP
# X-API-Language: Ch
# X-API-Matching: c50dddad6238e34da42c588bd6f884a3
# Authorization: 10b65929bb22a589b9c7bfc205343685
# X-Client-OS: Android
# Host: kjxq.api.wlnps.com
# Connection: Keep-Alive
# Accept-Encoding: gzip
# User-Agent: okhttp/4.9.0
url = 'https://kjxq.api.wlnps.com/filter/allNames'
header = {
    'X-Client-Version': '1.3.2',
    'X-Client-Time': '1629355712100',
    # 'X-Device-Flag': '7dcca9b1-dc07-4bde-aebf-caa462ffbb93',
    'X-Client-Model': 'HUAWEIVOG-AL10',
    'X-API-Version': '1',
    'X-Client-App-Id': 'com.mjxq.app',
    'X-Client-Type': 'APP',
    'X-API-Language': 'Ch',
    'X-API-Matching': 'c50dddad6238e34da42c588bd6f884a3',
    'Authorization': '10b65929bb22a589b9c7bfc205343685',
    'X-Client-OS': 'Android',
    'Host': 'kjxq.api.wlnps.com',
    # 'Connection': 'Keep-Alive',
    # 'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.9.0'
}
# resp = requests.get(url, headers=header)
# print(resp.text)

# 推荐
recommend_url = 'https://kjxq.api.wlnps.com/home/recommend/v2'
resp = requests.get(recommend_url, headers=header, verify=False)
print(resp.text)

# 搜索
search_url = 'https://kjxq.api.wlnps.com/filter/hint'
header['Content-Type'] = 'application/json; charset=utf-8'
payload = {
    'name': '神盾局'
}
resp = requests.post(search_url, json.dumps(payload), headers=header, verify=False)
print(resp.text)

# 列表
list_url = 'https://kjxq.api.wlnps.com/ranks/list/v2'
header['Content-Type'] = 'application/json; charset=utf-8'
payload = {"type": -2, "page": 1, "size": 5}
resp = requests.post(list_url, json.dumps(payload), headers=header, verify=False)
print(resp.text)

# 影片信息
movie_info_url = 'https://kjxq.api.wlnps.com/movie/info'
header['Content-Type'] = 'application/json; charset=utf-8'
payload = {
    "movie_id": 5214
}
resp = requests.post(movie_info_url, data=json.dumps(payload), headers=header, verify=False)
print(resp.text)

# 播放地址
play_path = 'https://kjxq.api.wlnps.com/movie/path'
header['Content-Type'] = 'application/json; charset=utf-8'
payload = {"episode": 1, "id": 5214}
resp = requests.post(play_path, data=json.dumps(payload), headers=header, verify=False)
print(resp.text)
