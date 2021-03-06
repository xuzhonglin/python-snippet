#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/20 11:01
@Author   : colinxu
@File     : server.py
@Desc     : mjxq 接口服务
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from movie import Movie
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)

MOVIE = Movie()
PREFIX = ''


@app.route(PREFIX + '/', methods=['GET', 'POST'])
def index():
    return _response(msg='It is working')


@app.route(PREFIX + '/list', methods=['GET', 'POST'])
def get_all_list():
    page_no = _parse_params('page')
    if _is_blank(page_no):
        return _response(msg='page is null')
    list_result = MOVIE.all_list(int(page_no))
    return _response(list_result)


@app.route(PREFIX + '/recommend', methods=['GET', 'POST'])
def get_recommend_list():
    recommend_result = MOVIE.recommend_list()
    return _response(recommend_result)


@app.route(PREFIX + '/filter/keywords', methods=['GET', 'POST'])
def get_filter_keywords():
    filter_keywords = MOVIE.filter_keywords()
    return _response(filter_keywords)


@app.route(PREFIX + '/filter/condition', methods=['GET', 'POST'])
def get_filter_condition():
    filter_condition = MOVIE.filter_condition()
    return _response(filter_condition)


@app.route(PREFIX + '/filter/search', methods=['GET', 'POST'])
def get_filter_search():
    condition = _parse_params()
    if condition is None:
        return _response(msg='condition is null')
    filter_search_result = MOVIE.filter_search(condition)
    return _response(filter_search_result)


@app.route(PREFIX + '/search', methods=['GET', 'POST'])
def search_movie():
    keyword = _parse_params('keyword')
    if _is_blank(keyword):
        return _response(msg='keyword is null')
    search_result = MOVIE.search(keyword)
    return _response(search_result)


@app.route(PREFIX + '/info', methods=['GET', 'POST'])
def get_movie_info():
    movie_id = _parse_params('id')
    if _is_blank(movie_id):
        return _response(msg='id is null')
    movie_info = MOVIE.info(int(movie_id))
    return _response(movie_info)


@app.route(PREFIX + '/play', methods=['POST'])
def get_play_url():
    episode = _parse_params()
    if episode is None:
        return _response(msg='episode is null')
    play_url = MOVIE.play(episode)
    # if play_url is not None and not _is_blank(play_url['play_path']):
    #     play_url['play_path'] = request.host_url + 'm3u8?source=' + play_url['play_path']
    return _response(play_url)


@app.route(PREFIX + '/m3u8', methods=['GET', 'POST'])
def m3u8():
    url = _parse_params('source')
    e = _parse_params('e')
    token = _parse_params('token')
    final_url = '{}&e={}&token={}'.format(url, e, token)
    resp = requests.get(final_url)
    header = {}
    for item in resp.headers:
        header[item] = resp.headers.get(item)
    # print(resp.text)
    resp = resp.text.replace('http://', 'https://')
    return resp, 200, header


@app.route('/lib/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


def _is_blank(s):
    if type(s) == int:
        return s is None
    elif type(s) == str:
        return s is None or len(s) == 0


def _response(data=None, msg: str = 'success', code: int = 200):
    ret = {
        'code': code,
        'msg': msg
    }
    if data is not None:
        ret['data'] = data

    return jsonify(ret), code


def _parse_params(name: str = None):
    if request.method == 'POST':
        if name is None:
            return request.json
        return request.json[name]
    elif request.method == 'GET':
        return request.args.get(name)
    else:
        return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10820)
