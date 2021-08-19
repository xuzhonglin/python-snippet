#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/15 12:30
@Author   : colinxu
@File     : checkin.py
@Desc     : 自动签到
"""

import requests
from message import Message


class Checkin:
    URL = ''
    USERNAME = ''
    PASSWORD = ''

    SESS = requests.session()

    def __init__(self, config: dict):
        self.URL = config['url']
        self.USERNAME = config['username']
        self.PASSWORD = config['password']
        self.is_login = False
        self.config = config
        self._login()

    def _login(self):
        """
        登录系统
        :return:
        """
        if self.is_login:
            return
        url = self.URL + '/auth/login'
        payload = {
            'email': self.USERNAME,
            'passwd': self.PASSWORD,
            'remember_me': 'on',
            'code': ''
        }
        resp = self.SESS.post(url, payload)
        resp = resp.json()
        self.is_login = True
        print(resp)

    def checkin(self):
        """
        签到
        :return:
        """
        if not self.is_login:
            return
        url = self.URL + '/user/checkin'
        resp = self.SESS.post(url)
        resp = resp.json()
        if resp['ret'] == 1:
            message = Message(self.config)
            message.send(self.config['mess_title'], resp['msg'])
        print(resp)
        return resp
