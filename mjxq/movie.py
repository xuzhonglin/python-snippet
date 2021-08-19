#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/19 19:08
@Author   : colinxu
@File     : movie.py
@Desc     : mjxq 电影
"""
import requests
import json
import api as API

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

    def search(self, name: str):
        """
        搜索影片
        :param name: 关键字
        :return: list 结果列表
        """
        payload = {
            'name': name
        }
        resp = self._post(API.MOVIE_SEARCH, payload)
        # print(resp.text)
        resp = resp.json()
        return resp['data']

    def info(self, movie_id: int):
        """
        获取影片详情
        :param movie_id: 影片的id
        :return:
        """
        payload = {
            "movie_id": movie_id
        }
        resp = self._post(API.MOVIE_INFO, payload)
        # print(resp.text)
        resp = resp.json()
        return resp['data']

    def play(self, episode):
        payload = {
            'episode': episode['episode'],
            'id': episode['movie_id']
        }
        resp = self._post(API.MOVIE_PLAY, payload)
        # print(resp.text)
        resp = resp.json()
        return resp['data']

    def _get(self, url):
        url = BASE_URL + url
        header = HEADER
        return requests.get(url, headers=header, verify=False)

    def _post(self, url, data):
        url = BASE_URL + url
        header = HEADER
        header['Content-Type'] = 'application/json; charset=utf-8'
        return requests.post(url, json.dumps(data), headers=header, verify=False)


if __name__ == '__main__':
    movie = Movie()
    a = movie.search('肖申克')
    print(a)

    b = movie.info(a[0]['id'])
    print(b)

    c = movie.play(b['episode'][0])
    print(c)
