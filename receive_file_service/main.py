#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/8/18 10:20
@Author   : colinxu
@File     : main.py
@Desc     : 接收文件服务
"""

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return 'Service is Working!', 200


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    file.save(file_name)
    return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20311)
