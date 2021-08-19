#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/19 19:08
@Author   : colinxu
@File     : movie.py
@Desc     : 电影
"""
import requests
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = 'https://kjxq.api.wlnps.com'
HEADER = {
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
    'User-Agent': 'okhttp/4.9.0'
}


class Movie:

    def __init__(self):
        pass

    def search(self, name):
        search_url = BASE_URL + '/filter/hint'
        header = HEADER
        header['Content-Type'] = 'application/json; charset=utf-8'
        payload = {
            'name': name
        }
        resp = requests.post(search_url, json.dumps(payload), headers=header, verify=False)
        print(resp.text)
        resp = resp.json()
        return resp['data']

    def info(self, movie_id):
        pass

    def play(self, movie_id):
        pass

    def _get_play_url(self, id):
        pass


if __name__ == '__main__':
    movie = Movie()
    a = movie.search('肖申克')
    print(a)
