#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/15 12:36
@Author   : colinxu
@File     : message.py
@Desc     : 发送消息
        # 及时达 http://push.ijingniu.cn/
        # server酱 https://sct.ftqq.com
"""
import requests


class Message:
    MESS_TYPE = ''
    MESS_KEY = ''

    def __init__(self, config: dict):
        self.MESS_TYPE = config['mess_type']
        self.MESS_KEY = config['mess_key']

    def _parse_url(self):
        """
        转换要发送的url
        :return:
        """
        send_url = ''
        if self.MESS_TYPE == 'JSD':
            send_url = 'http://push.ijingniu.cn/send'
        elif self.MESS_TYPE == 'SERVER':
            send_url = 'https://sct.ftqq.com/%s.send'.format(self.MESS_KEY)
        return send_url

    def _parse_payload(self, title, message):
        """
        包装消息体
        :param title: 标题
        :param message: 消息内容
        :return:
        """
        payload = {}
        if self.MESS_TYPE == 'JSD':
            payload = {
                'key': self.MESS_KEY,
                'head': title,
                'body': message
            }
        elif self.MESS_TYPE == 'SERVER':
            payload = {
                'title': title,
                'desp': message
            }
        return payload

    def send(self, title: str, message: str):
        """
        发送消息
        :param title: 标题
        :param message: 消息内容
        :return:
        """
        url = self._parse_url()
        payload = self._parse_payload(title, message)
        resp = requests.post(url, payload)
        return resp.json()
