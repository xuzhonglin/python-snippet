#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/14 17:14
@Author   : colinxu
@File     : auto_sign.py
@Desc     : fswk 自动签到
"""
import requests

URL = 'https://yz.fswk.net'

USERNAME = 'xuzhonglin@outlook.com'
PASSWORD = 'xzl961028*#'

SESS = requests.session()


def login():
    url = URL + '/auth/login'
    payload = {
        'email': USERNAME,
        'passwd': PASSWORD,
        'remember_me': 'on',
        'code': ''
    }
    resp = SESS.post(url, payload)
    resp = resp.json()
    print(resp)


def sign():
    url = URL + '/user/checkin'
    resp = SESS.post(url)
    resp = resp.json()
    print(resp)


if __name__ == '__main__':
    login()
    sign()
