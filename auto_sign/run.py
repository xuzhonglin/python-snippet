#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/15 12:56
@Author   : colinxu
@File     : run.py
@Desc     : 执行入口
"""

from checkin import Checkin


def run():
    configs = [
        {
            'url': 'https://yz.fswk.net',
            'username': 'xuzhonglin@outlook.com',
            'password': 'xzl961028*#',
            'mess_type': 'JSD',
            'mess_key': '352352ed32614eba8589782442b9fdda',
            'mess_title': '自动签到成功（fswk）'
        }, {
            'url': 'https://fastlink.ws',
            'username': 'xuzhonglinx@gmail.com',
            'password': 'xzl961028*#',
            'mess_type': 'JSD',
            'mess_key': '352352ed32614eba8589782442b9fdda',
            'mess_title': '自动签到成功（FastLink）'
        }
    ]

    for item in configs:
        checkin = Checkin(item)
        checkin.checkin()
