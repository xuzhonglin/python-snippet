#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/19 21:58
@Author   : colinxu
@File     : api.py
@Desc     : mjxq 的 api
"""
# 搜索接口
MOVIE_SEARCH = '/filter/hint'
# 获取电影信息
MOVIE_INFO = '/movie/info'
# 获取电影播放地址
MOVIE_PLAY = '/movie/path'
# 获取电影列表
MOVIE_LIST = '/ranks/list/v2'
# 获取推荐
MOVIE_RECOMMEND = '/home/recommend/v2'
# 获取电影的类别：美剧 英剧
MOVIE_CATEGORY = '/types/platform'
# 筛选条件
MOVIE_FILTER_CONDITION = '/types/screen'
# 根据筛选条件搜索
MOVIE_FILTER_SEARCH = '/filter/movies'
# 所有电影关键字
MOVIE_FILTER_KEYWORDS = '/filter/allNames'
