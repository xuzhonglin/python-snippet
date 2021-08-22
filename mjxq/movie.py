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

LOG_ENABLE = True

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
        self._log(resp.text)
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
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def play(self, episode):
        """
        获取播放地址
        :param episode: 剧集
        :return:
        """
        payload = {
            'episode': self._get_or_default(episode, 'episode', -1),
            'id': self._get_or_default(episode, 'movie_id', -1),
        }
        resp = self._post(API.MOVIE_PLAY, payload)
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def recommend_list(self):
        """
        获取推荐列表
        :return:
        """
        resp = self._get(API.MOVIE_RECOMMEND)
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def all_list(self, page: int = 1):
        """
        所有电影列表
        :param page: 页码
        :return:
        """
        payload = {
            "type": -2,
            "page": page,
        }
        resp = self._post(API.MOVIE_LIST, payload)
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def category(self):
        """
        获取电影的类别
        :return:
        """
        resp = self._get(API.MOVIE_CATEGORY)
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def filter_keywords(self):
        """
        获取所有关键字
        :return:
        """
        resp = self._get(API.MOVIE_FILTER_KEYWORDS)
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def filter_condition(self):
        """
        获取筛选条件
        :return:
        """
        resp = self._get(API.MOVIE_FILTER_CONDITION)
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def filter_search(self, condition: dict):
        """
        根据少选条件 筛选电影
        :param condition:  条件
        :return:
        """
        payload = {
            "complete_type": self._get_or_default(condition, 'complete_type', 0),
            "platform_type": self._get_or_default(condition, 'platform_type', 0),
            "movies_type": self._get_or_default(condition, 'movies_type', 0),
            "page": self._get_or_default(condition, 'page', 1),
            "sort_type": self._get_or_default(condition, 'sort_type', 0),
        }
        resp = self._post(API.MOVIE_FILTER_SEARCH, payload)
        self._log(resp.text)
        resp = resp.json()
        return resp['data']

    def _get_or_default(self, obj: dict, key: str, default):
        if key in obj:
            return obj[key]
        else:
            return default

    def _log(self, s):
        if LOG_ENABLE:
            print(s)

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

    d = movie.recommend_list()
    print(d)

    e = movie.all_list(2)
    print(e)

    f = movie.category()
    print(f)

    g = movie.filter_condition()
    print(g)

    h = movie.filter_search({})
    print(h)
